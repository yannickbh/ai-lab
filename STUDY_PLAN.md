# Plano de Estudo: CrewAI FDE - 30 Dias

> **Status Atual**: ✅ Setup Inicial Completo - Pronto para começar Dia 1-2
> 
> **Última Atualização**: 2026-01-10
> **Progresso Geral**: 0/30 dias (0%) - Setup completo, início do aprendizado

---

## Visão Geral
Este plano de 30 dias leva você de zero em CrewAI hands-on para um nível de competência prática em sistemas agenticos enterprise-ready. O projeto de referência é um **Enterprise Ticket Triage + Resolution Assistant** que exercita todos os blocos de aprendizado.

### Status Atual do Projeto
- ✅ **Estrutura do projeto criada** (`ai-lab/enterprise_ticket_assistant/`)
- ✅ **Dependências instaladas** (CrewAI v1.8.0, todas as bibliotecas necessárias)
- ✅ **Environment loader configurado** (detecta `.env` automaticamente)
- ✅ **Documentação completa** (README, Debug Playbook, Evaluation Guide)
- ✅ **Scripts de verificação** (`scripts/verify_install.py`, `scripts/check_env.py`)
- 🚀 **Pronto para começar Dia 1-2!**

---

## Projeto de Referência: Enterprise Ticket Assistant

### Descrição
Sistema multi-agente que tria, analisa e resolve tickets de suporte usando:
- Multi-agent crew (router/planner/executor/critic)
- Tool calls para APIs mock (CRM/ERP/KB)
- Memory + RAG para histórico e base de conhecimento
- Guardrails & evaluation (Pydantic schemas, policy checks)
- Observability completa (structlog, OpenTelemetry, métricas)
- Reliability (timeouts, retries, idempotency, circuit breakers)
- Security (redaction, tenant isolation, PII handling)
- Testes e validação end-to-end

### Localização do Projeto
**Diretório**: `ai-lab/enterprise_ticket_assistant/`

**Estrutura principal**:
- `src/` - Código fonte organizado por módulos
- `tests/` - Testes (unit, integration, evaluation)
- `docs/` - Documentação completa
- `config/` - Configurações YAML
- `scripts/` - Scripts utilitários de setup e verificação
- `mocks/` - APIs mock para desenvolvimento e testes

---

## Fase 1: Fundações CrewAI (Dias 1-7)

### Semana 1: CrewAI Hands-on Básico

**Dia 1-2: Setup e Primeiros Passos**
- [x] Ambiente virtual, dependências básicas ✅ **COMPLETO** (15/15 pacotes instalados)
- [x] Environment loader configurado ✅ **COMPLETO** (`.env` detectado automaticamente)
- [ ] Hello World com CrewAI (Agent/Task/Crew simples) - **PRÓXIMO PASSO**
- [ ] Entender Process.sequential vs hierárquico
- [ ] Criar primeiro mini-project: "Todo List Manager Agent"
- **Validação**: Agente cria, lista e completa tarefas via CrewAI

**Recursos para Dia 1-2:**
- Ver: `GETTING_STARTED.md` para guia detalhado
- Projeto: `ai-lab/enterprise_ticket_assistant/`
- Verificar setup: `python scripts/verify_install.py`
- Verificar env: `python scripts/check_env.py`

**Dia 3-4: Tools e Tool Calling**
- [ ] Criar ferramentas customizadas (Python functions como tools)
- [ ] Tool error handling e validação
- [ ] Safe tool design (sanitização, limites)
- [ ] Integrar com API mock simples (httpx)
- **Validação**: Agente usa tools corretamente, lida com erros graciosamente

**Recursos para Dia 3-4:**
- Diretório: `src/tools/` - Criar tools customizadas aqui
- Mock APIs: `mocks/` - Criar endpoints mock para testes
- Docs CrewAI Tools: https://docs.crewai.com/concepts/tools

**Dia 5-6: Multi-Agent Workflows**
- [ ] Criar crew com múltiplos agentes (router → executor → reviewer)
- [ ] Dependency management entre tasks (context parameter)
- [ ] Parallel vs sequential execution
- [ ] Task outputs como inputs para próximas tasks
- **Validação**: Workflow completo com 3+ agentes executando em ordem correta

**Recursos para Dia 5-6:**
- Diretórios: `src/agents/`, `src/tasks/`, `src/crew/`
- Exemplo já criado: `postLinkedin.py` (router → redator → editor)
- Docs: Process.sequential vs hierarchical em `.cursorrules`

**Dia 7: Semana 1 Review**
- [ ] Revisar código, documentar aprendizados
- [ ] Criar testes básicos (pytest) - usar `tests/unit/`
- [ ] Debug sem UI: logs estruturados básicos
- [ ] Executar: `python scripts/verify_install.py` para garantir tudo OK
- **Checkpoint**: Sistema funcional com multi-agent crew básico

**O que deve funcionar ao final da Semana 1:**
- ✅ Agente cria, lista e completa tarefas
- ✅ Tools customizadas funcionando
- ✅ Workflow multi-agent com 3+ agentes
- ✅ Testes básicos passando
- ✅ Logs estruturados básicos funcionando

---

## Fase 2: Reliability & Robustness (Dias 8-14)

### Semana 2: Prevenindo Falhas Emergentes

**Dia 8-9: Emergent Failure Modes**
- [ ] Simular loops infinitos, detectar patterns
- [ ] Implementar max_iterations e max_execution_time
- [ ] Timeout handling em tasks e tools
- [ ] Circuit breaker básico
- **Validação**: Sistema para em condições de loop/custo excessivo

**Dia 10-11: Determinism & Validation**
- [ ] Pydantic schemas para output validation (já instalado: v2.11.10)
- [ ] Constrained prompts (role/goal/backstory precisos)
- [ ] Output parsing e schema enforcement
- [ ] Fallback strategies quando validação falha
- **Validação**: Outputs sempre em formato esperado, fallbacks funcionam

**Recursos para Dia 10-11:**
- Pydantic já instalado e pronto para usar
- Exemplos em `.cursorrules` sobre output validation
- Ver: https://docs.pydantic.dev/ para schemas avançados

**Dia 12-13: Async & Concurrency**
- [ ] Converter para asyncio (async agents/tasks)
- [ ] Concurrency control (semáforos, locks)
- [ ] Timeout em async operations
- [ ] Race condition testing
- **Validação**: Múltiplos tickets processados em paralelo com controle

**Dia 14: Semana 2 Review**
- [ ] Stress testing (100+ tickets)
- [ ] Análise de custos (tracking token usage)
- [ ] Documentar tradeoffs: autonomia vs controle
- **Checkpoint**: Sistema robusto contra falhas comuns

---

## Fase 3: Integrations & Reliability (Dias 15-21)

### Semana 3: Integrações Enterprise-Grade

**Dia 15-16: Retries & Idempotency**
- [ ] Implementar retries com tenacity (exponential backoff)
- [ ] Idempotency keys para operações críticas
- [ ] De-duplication de requests
- [ ] Idempotency testing (duplicate requests não causam side effects)
- **Validação**: Sistema lida com falhas temporárias, operações são idempotentes

**Dia 17-18: Rate Limiting & Resilience**
- [ ] Rate limit strategies (batching, queuing, throttling)
- [ ] aiolimiter para controle de taxa
- [ ] Exponential backoff para rate limit errors
- [ ] Redis (opcional) para distributed rate limiting
- **Validação**: Sistema não excede rate limits, backoff funciona

**Dia 19-20: Secure Integrations**
- [ ] OAuth/JWT para APIs
- [ ] Webhook signature validation
- [ ] Secrets management (python-dotenv, environment variables)
- [ ] Secure credential handling (nunca logar secrets)
- **Validação**: Autenticação segura, secrets não vazam em logs

**Dia 21: Semana 3 Review**
- [ ] Integration testing com APIs mock
- [ ] Performance benchmarking
- [ ] Cost tracking (tokens por operação)
- **Checkpoint**: Integrações robustas e seguras

---

## Fase 4: Memory, RAG & Context Management (Dias 22-28)

### Semana 4: Context e RAG

**Dia 22-23: Memory & Context Windows**
- [ ] Short-term memory (conversation context)
- [ ] Long-term memory (persistent storage) - usar SQLite/PostgreSQL
- [ ] Context summarization para reduzir tokens
- [ ] Token counting e cost estimation
- **Validação**: Context gerenciado eficientemente, custos controlados

**Recursos para Dia 22-23:**
- Diretório: `src/memory/` - Implementar gerenciamento de memória
- Config: `config/config.yaml` - Configurações de memória já definidas
- DATABASE_URL: Definir em `.env` (padrão: SQLite)

**Dia 24-25: RAG Pipeline Básico**
- [ ] Embeddings (sentence-transformers) ✅ **JÁ INSTALADO**
- [ ] Vector store (Qdrant/Chroma/Weaviate) ✅ **Qdrant instalado**
- [ ] Retrieval (semantic search)
- [ ] Reranking (opcional, se necessário)
- [ ] Quando NÃO usar RAG (critérios de decisão)
- **Validação**: RAG retorna contexto relevante, melhorando respostas

**Recursos para Dia 24-25:**
- Diretório: `src/rag/` - Implementar pipeline RAG
- Qdrant: Configurar em `.env` (QDRANT_URL, padrão: localhost:6333)
- sentence-transformers: Modelo padrão `all-MiniLM-L6-v2` já disponível
- Config: `config/config.yaml` - Configurações RAG já definidas

**Dia 26-27: Integration RAG + CrewAI**
- [ ] RAG tool para agentes
- [ ] Knowledge base para histórico de tickets
- [ ] Similar ticket retrieval
- [ ] Context injection em prompts
- **Validação**: Agentes usam conhecimento histórico efetivamente

**Dia 28: Semana 4 Review**
- [ ] RAG evaluation (precision/recall)
- [ ] Token cost analysis (com vs sem RAG)
- [ ] Context bloat prevention
- **Checkpoint**: Sistema com memória e RAG funcional

---

## Fase 5: Security, Guardrails & Observability (Dias 29-30)

### Semana 5: Enterprise Readiness

**Dia 29: Security & Guardrails**
- [ ] PII redaction (regex + NLP)
- [ ] Tenant isolation (multi-tenancy seguro)
- [ ] Prompt injection prevention
- [ ] Output sanitization
- [ ] Policy checks (pydantic validators) ✅ **Pydantic já instalado**
- **Validação**: PII não vaza, tenants isolados, outputs seguros

**Recursos para Dia 29:**
- Diretório: `src/security/` - Implementar segurança
- Config: `config/config.yaml` - Configurações de segurança já definidas
- Environment loader: Já implementado com suporte a tenant isolation

**Dia 30: Observability & Governance**
- [ ] Structured logging (structlog) ✅ **JÁ INSTALADO**
- [ ] OpenTelemetry tracing ✅ **JÁ INSTALADO**
- [ ] Prometheus metrics (cost, latency, success rate) ✅ **JÁ INSTALADO**
- [ ] Cost KPIs (tokens por ticket, custo por sucesso)
- [ ] Debug playbook (troubleshooting sem UI) ✅ **JÁ CRIADO** (`docs/debug_playbook.md`)
- [ ] Evaluation harness (golden set, regression tests) ✅ **GUIA CRIADO** (`docs/evaluation.md`)
- **Validação**: Sistema observável, métricas coletadas, debug possível

**Recursos para Dia 30:**
- Diretório: `src/observability/` - Implementar logging, tracing, metrics
- Debug Playbook: `docs/debug_playbook.md` - Já documentado
- Evaluation Guide: `docs/evaluation.md` - Já documentado
- Config: `config/config.yaml` - Configurações de observability já definidas

---

## Marcos Principais

### Marco 1 (Dia 7): Fundações CrewAI
- ✅ Multi-agent crew funcional
- ✅ Tools básicos implementados
- ✅ Workflow end-to-end simples

### Marco 2 (Dia 14): Reliability
- ✅ Proteção contra loops e custos excessivos
- ✅ Validação de outputs
- ✅ Async operations estáveis

### Marco 3 (Dia 21): Integrações
- ✅ Retries e idempotency
- ✅ Rate limiting
- ✅ Autenticação segura

### Marco 4 (Dia 28): RAG & Memory
- ✅ Pipeline RAG completo
- ✅ Context management eficiente
- ✅ Memória persistente

### Marco 5 (Dia 30): Enterprise Ready
- ✅ Security implementada
- ✅ Observability completa
- ✅ Testes e avaliação
- ✅ Documentação e playbooks

---

## Projeto Final: Enterprise Ticket Assistant

Ao final dos 30 dias, você terá um sistema completo que:

1. **Tria tickets** automaticamente (router agent)
2. **Planeja resolução** (planner agent)
3. **Executa ações** via APIs (executor agent)
4. **Revisa qualidade** (critic agent)
5. **Aprende do histórico** (RAG + memory)
6. **É observável** (logs, traces, metrics)
7. **É resiliente** (retries, timeouts, circuit breakers)
8. **É seguro** (PII handling, tenant isolation)
9. **É testável** (evaluation harness, golden set)

---

## Próximos Passos (Dias 31-60 - Opcional Extensão)

- HITL (Human-in-the-Loop) patterns
- Advanced evaluation (LLM-as-judge, critic loops)
- Production deployment (Docker, Kubernetes)
- Multi-tenant scaling
- Advanced RAG (reranking, hybrid search)
- Fine-tuning strategies
- Cost optimization (model selection, caching)

---

## Como Usar Este Plano

1. **Siga dia a dia** - Cada dia tem tarefas específicas
2. **Valide sempre** - Execute os testes de validação
3. **Documente aprendizados** - Mantenha notes sobre tradeoffs
4. **Debug sem UI** - Force-se a usar logs/code, não UI tools (ver Debug Playbook)
5. **Questione tradeoffs** - Sempre pergunte "por que esta escolha?"

### Quick Start (Se ainda não começou)

```bash
# 1. Navegar para o projeto
cd ai-lab/enterprise_ticket_assistant

# 2. Verificar instalação (deve mostrar 15/15 OK)
python scripts/verify_install.py

# 3. Verificar variáveis de ambiente (.env)
python scripts/check_env.py

# 4. Começar Dia 1: Criar Hello World
# Ver GETTING_STARTED.md para detalhes
```

### Progresso Atual
- **Setup Inicial**: ✅ Completo (Dia 0)
- **Dia 1-2**: 🔄 Próximo passo - Hello World CrewAI
- **Dias 3-30**: ⏳ Aguardando

### Dicas Importantes
- ⚠️ **Não pule etapas** - Cada semana constrói sobre a anterior
- 📝 **Documente decisões** - Mantenha notes sobre por que escolheu cada abordagem
- 🐛 **Use o Debug Playbook** - Quando tiver problemas, consulte `docs/debug_playbook.md`
- 💰 **Monitore custos** - Sempre rastreie uso de tokens desde o início
- ✅ **Valide checkpoints** - Execute validações semanais para garantir progresso

---

## Recursos Adicionais

### Documentação do Projeto
- **Getting Started**: [`GETTING_STARTED.md`](GETTING_STARTED.md) - Guia de início rápido
- **Project Summary**: [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) - Visão geral executiva
- **Debug Playbook**: [`ai-lab/enterprise_ticket_assistant/docs/debug_playbook.md`](ai-lab/enterprise_ticket_assistant/docs/debug_playbook.md) - Como debugar sem UI
- **Evaluation Guide**: [`ai-lab/enterprise_ticket_assistant/docs/evaluation.md`](ai-lab/enterprise_ticket_assistant/docs/evaluation.md) - Métricas e avaliação
- **Environment Setup**: [`ai-lab/enterprise_ticket_assistant/docs/ENV_SETUP.md`](ai-lab/enterprise_ticket_assistant/docs/ENV_SETUP.md) - Configuração de variáveis
- **Project README**: [`ai-lab/enterprise_ticket_assistant/README.md`](ai-lab/enterprise_ticket_assistant/README.md) - Arquitetura do projeto

### Scripts Úteis
- `python scripts/verify_install.py` - Verificar instalação de dependências
- `python scripts/check_env.py` - Verificar variáveis de ambiente
- `python -m src.main --ticket-id 12345` - Executar assistente (após implementação)

### Documentação Externa
- **CrewAI Docs**: https://docs.crewai.com
- **CrewAI Tools**: https://github.com/joaomdmoura/crewAI-tools
- **Pydantic Docs**: https://docs.pydantic.dev/ (validação de outputs)
- **Structlog Docs**: https://www.structlog.org/ (logging estruturado)
- **OpenTelemetry**: https://opentelemetry.io/docs/ (tracing)

### Estrutura do Projeto
```
enterprise_ticket_assistant/
├── src/              # Código fonte
│   ├── agents/       # Semana 1: Definir agents aqui
│   ├── tasks/        # Semana 1: Definir tasks aqui
│   ├── tools/        # Semana 1-2: Criar tools aqui
│   ├── crew/         # Semana 1: Criar crew aqui
│   └── ...
├── tests/            # Testes (unit, integration, evaluation)
├── docs/             # Documentação completa
├── config/           # Configurações YAML
└── scripts/          # Scripts utilitários
```
