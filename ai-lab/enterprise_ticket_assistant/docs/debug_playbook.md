# Debug Playbook: Enterprise Ticket Assistant

Este playbook descreve como debugar problemas no sistema **sem usar UI tools**, focando em logs estruturados, traces e code-level debugging.

---

## 1. Problemas Comuns e Soluções

### 1.1 Agente em Loop Infinito

**Sintomas:**
- Task executa por muito tempo (>5 min)
- Logs mostram mesma mensagem repetida
- Custo de tokens cresce rapidamente

**Debug Steps:**
```bash
# 1. Verificar logs estruturados
grep "agent_name" logs/ticket_assistant.log | tail -20

# 2. Verificar métricas de iterações
curl http://localhost:8000/metrics | grep "agent_iterations_total"

# 3. Verificar traces OpenTelemetry
# (Se configurado, usar Jaeger/OTEL Collector UI)

# 4. Inspecionar código do agente
python -c "from src.agents.router import router_agent; print(router_agent.max_iterations)"
```

**Soluções:**
- Verificar `max_iterations` no Agent/Task
- Verificar `max_execution_time` na Crew
- Adicionar early exit conditions na task description
- Implementar circuit breaker

---

### 1.2 Output Validation Falhando

**Sintomas:**
- Task falha com `ValidationError`
- Output não segue schema esperado
- Agente não retorna formato correto

**Debug Steps:**
```python
# 1. Verificar schema Pydantic
from src.tasks.triage import TriageTaskOutput
print(TriageTaskOutput.schema_json(indent=2))

# 2. Inspecionar output raw
import structlog
logger = structlog.get_logger()
logger.info("raw_output", output=raw_output)

# 3. Testar validação manualmente
try:
    validated = TriageTaskOutput.parse_raw(json_output)
except ValidationError as e:
    print(f"Validation errors: {e.errors()}")
```

**Soluções:**
- Ajustar schema Pydantic para ser mais permissivo
- Melhorar prompt/description da task
- Adicionar exemplos no prompt
- Implementar fallback/retry com schema mais flexível

---

### 1.3 Tool Calls Falhando

**Sintomas:**
- Erro ao chamar API externa
- Rate limit errors
- Timeout em chamadas HTTP

**Debug Steps:**
```python
# 1. Verificar logs de HTTP
grep "httpx" logs/ticket_assistant.log | grep -E "ERROR|WARN"

# 2. Verificar métricas de rate limiting
curl http://localhost:8000/metrics | grep "rate_limit"

# 3. Testar tool isoladamente
python -c "from src.tools.crm_api import update_ticket; update_ticket(ticket_id='123', status='open')"

# 4. Verificar circuit breaker status
curl http://localhost:8000/metrics | grep "circuit_breaker"
```

**Soluções:**
- Verificar rate limits (aiolimiter)
- Implementar retries com exponential backoff
- Ajustar timeouts
- Verificar circuit breaker não está aberto

---

### 1.4 RAG Retornando Resultados Irrelevantes

**Sintomas:**
- Contexto retornado não relacionado
- Embeddings de baixa qualidade
- Similaridade muito baixa

**Debug Steps:**
```python
# 1. Verificar embeddings
from src.rag.embeddings import get_embedding
query_emb = get_embedding("user query")
print(f"Embedding dim: {len(query_emb)}")

# 2. Testar busca no vector store
from src.rag.retrieval import search_kb
results = search_kb("user query", top_k=5)
for r in results:
    print(f"Score: {r.score}, Text: {r.text[:100]}")

# 3. Verificar índice do vector store
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6333")
collections = client.get_collections()
print(collections)
```

**Soluções:**
- Re-indexar documentos
- Ajustar `similarity_threshold`
- Tentar modelo de embedding diferente
- Habilitar reranking

---

### 1.5 Memory/Context Bloat

**Sintomas:**
- Tokens aumentando exponencialmente
- Context window excedido
- Custo muito alto

**Debug Steps:**
```python
# 1. Verificar token usage
from src.observability.metrics import get_token_usage
usage = get_token_usage(tenant_id="acme")
print(f"Total tokens: {usage.total}, Cost: ${usage.cost_usd}")

# 2. Verificar tamanho do context
from src.memory.context import get_context_size
size = get_context_size(conversation_id="conv_123")
print(f"Context size: {size} tokens")

# 3. Verificar se summarization está ativa
grep "summarize" logs/ticket_assistant.log
```

**Soluções:**
- Habilitar summarization automática
- Reduzir `max_context_tokens`
- Limpar contexto antigo
- Usar sliding window

---

## 2. Structured Logging

### 2.1 Configuração

```python
import structlog

logger = structlog.get_logger()
logger.info(
    "ticket_processed",
    ticket_id="12345",
    tenant_id="acme",
    agent="router",
    execution_time_ms=1234,
    tokens_used=567,
    cost_usd=0.001
)
```

### 2.2 Buscar em Logs

```bash
# Buscar por ticket_id
grep '"ticket_id": "12345"' logs/ticket_assistant.log

# Buscar erros de um tenant
grep '"tenant_id": "acme"' logs/ticket_assistant.log | grep ERROR

# Buscar por agente
grep '"agent": "router"' logs/ticket_assistant.log

# Analisar performance
grep "execution_time_ms" logs/ticket_assistant.log | jq 'select(.execution_time_ms > 5000)'
```

---

## 3. Métricas Prometheus

### 3.1 Métricas Principais

```bash
# Ver todas as métricas
curl http://localhost:8000/metrics

# Métricas específicas
curl http://localhost:8000/metrics | grep "ticket_assistant"

# Exemplos:
# - ticket_assistant_tasks_total{status="success"}
# - ticket_assistant_tokens_total{agent="router"}
# - ticket_assistant_cost_usd_total
# - ticket_assistant_execution_time_seconds
# - ticket_assistant_rate_limit_exceeded_total
```

### 3.2 Querying Prometheus (se configurado)

```promql
# Total de tickets processados (últimas 24h)
sum(rate(ticket_assistant_tasks_total[24h]))

# Custo por tenant
sum by (tenant_id) (ticket_assistant_cost_usd_total)

# Taxa de sucesso
sum(rate(ticket_assistant_tasks_total{status="success"}[5m])) 
/ 
sum(rate(ticket_assistant_tasks_total[5m]))
```

---

## 4. OpenTelemetry Traces

### 4.1 Verificar Traces

Se usando Jaeger ou similar:
```bash
# Verificar se traces estão sendo exportados
curl http://localhost:4317/v1/traces

# Query traces por ticket_id (via API Jaeger)
curl "http://localhost:16686/api/traces?service=ticket-assistant&tags=ticket_id:12345"
```

### 4.2 Analisar Span Tree

```
ticket_processing (root)
  ├── router_agent
  │   ├── search_kb (tool)
  │   └── classify_ticket (task)
  ├── planner_agent
  │   └── create_plan (task)
  └── executor_agent
      ├── update_crm (tool)
      └── send_email (tool)
```

---

## 5. Testes de Debug

### 5.1 Testar Agente Isoladamente

```python
from src.agents.router import create_router_agent
from crewai import Task

agent = create_router_agent()
task = Task(
    description="Classify ticket: {ticket_content}",
    expected_output="Classification with category and priority",
    agent=agent
)

result = task.execute(inputs={"ticket_content": "My API is down"})
print(result)
```

### 5.2 Testar Tool Isoladamente

```python
from src.tools.crm_api import update_ticket

try:
    result = update_ticket(ticket_id="123", status="open", tenant_id="acme")
    print(f"Success: {result}")
except Exception as e:
    print(f"Error: {e}")
    # Verificar logs, rate limits, circuit breaker
```

---

## 6. Checklist de Debug

Antes de pedir ajuda, verifique:

- [ ] Logs estruturados foram consultados
- [ ] Métricas Prometheus verificadas
- [ ] Traces OpenTelemetry analisados (se disponível)
- [ ] Tool foi testado isoladamente
- [ ] Agent foi testado isoladamente
- [ ] Rate limits verificados
- [ ] Circuit breaker status verificado
- [ ] Token usage/cost verificado
- [ ] Schema validation testado
- [ ] Variáveis de ambiente corretas

---

## 7. Comandos Úteis

```bash
# Ver últimas 50 linhas de log
tail -50 logs/ticket_assistant.log

# Buscar todos os erros
grep ERROR logs/ticket_assistant.log | tail -20

# Ver métricas em tempo real
watch -n 5 'curl -s http://localhost:8000/metrics | grep ticket_assistant'

# Testar endpoint mock
curl http://localhost:8080/api/tickets/12345

# Verificar saúde do sistema
curl http://localhost:8000/health
```

---

## 8. Recursos Adicionais

- [CrewAI Debugging Guide](https://docs.crewai.com/how-to/debugging)
- [Structlog Documentation](https://www.structlog.org/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Client Python](https://github.com/prometheus/client_python)
