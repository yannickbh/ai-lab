# Arquitetura: Enterprise Ticket Assistant

## Princípios de Design

### 1. Separation of Concerns (Separação de Responsabilidades)

Cada camada tem uma responsabilidade específica:

```
┌─────────────────────────────────────────┐
│  main.py / scripts/                     │  ← Entry Point (CLI/API)
│  - Parse arguments                       │
│  - Setup logging                         │
│  - Orchestrate execution                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  crew/                                  │  ← Orchestration Layer
│  - create_*_crew() functions            │
│  - Define workflow (agents + tasks)     │
│  - Configure Process (sequential/etc)   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  tasks/ + agents/                       │  ← Domain Layer
│  - tasks.py: Define WHAT to do          │
│  - agents.py: Define WHO does it        │
│  - Business logic, no orchestration     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  tools/                                 │  ← Infrastructure Layer
│  - External APIs                        │
│  - Database access                      │
│  - Utilities                            │
└─────────────────────────────────────────┘
```

### 2. Import Strategy

**Padrão: Imports Absolutos**
```python
# ✅ CORRETO
from src.agents.agents import hello_agent
from src.tasks.tasks import hello_task

# ❌ EVITAR (quando possível)
from .agents import hello_agent  # Relativos só dentro do mesmo pacote
```

**Por quê?**
- **Executável como script**: `python src/mainhello.py` funciona
- **Executável como módulo**: `python -m src.mainhello` funciona
- **IDE-friendly**: IntelliSense funciona corretamente
- **Testável**: Importa facilmente em testes
- **Explicito**: Fica claro de onde vem cada coisa

**Quando usar relativo?**
- Apenas dentro do mesmo pacote para evitar dependências circulares
- Exemplo: `from .helpers import something` dentro de `agents/helpers.py`

### 3. Factory Pattern para Crews

**Padrão: Factory Functions**
```python
def create_hello_crew():
    """Factory function - cria e retorna crew."""
    return Crew(...)

def create_ticket_crew(tenant_id: str, config: dict = None):
    """Factory function com parâmetros."""
    config = config or load_config()
    return Crew(...)
```

**Por quê?**
- **Lazy creation**: Crew só é criado quando necessário
- **Testável**: Fácil de mockar em testes
- **Configurável**: Pode receber parâmetros
- **Reutilizável**: Pode criar múltiplos crews diferentes
- **Não executa no import-time**: Evita side effects ao importar

### 4. Dependency Direction

**Regra: Dependências fluem UMA direção**

```
main.py
  → crew.py
     → tasks.py
     → agents.py
        → tools.py
           → utils.py
```

**Nunca fazer:**
- `agents.py` importar de `crew.py` (cria dependência circular)
- `tools.py` importar de `agents.py` (inverte dependência)

**Se precisar de referência circular:**
- Usar dependency injection
- Usar callbacks/functions
- Reorganizar estrutura

### 5. Configuration Management

**Padrão: Configuração em camadas**

1. **Environment Variables** (`.env`)
   - Secrets, API keys
   - URLs de serviços externos
   - Feature flags

2. **Config Files** (`config/config.yaml`)
   - Valores padrão
   - Configurações de negócio
   - Configurações de agentes/tasks

3. **Code Defaults**
   - Valores que nunca mudam
   - Lógica de fallback

```python
# Exemplo: Como priorizar
config_value = (
    os.getenv("CUSTOM_VALUE") or           # 1. Env var (mais alta prioridade)
    yaml_config.get("custom_value") or     # 2. Config file
    "default"                              # 3. Code default
)
```

### 6. Error Handling Strategy

**Camadas de tratamento:**

```python
# tools/ (Low level)
def call_api():
    try:
        response = httpx.get(...)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        # Log detalhado
        logger.error(f"API call failed: {e}")
        raise  # Propaga para camada superior

# agents/ (Mid level)
def agent_task():
    try:
        result = call_api()
        return process(result)
    except httpx.HTTPError:
        # Fallback ou retry
        return fallback_value()

# crew/ (High level)
def create_crew():
    # Configura timeouts, circuit breakers
    # Define fallbacks globais
```

## Estrutura de Arquivos Esperada

```
src/
├── agents/
│   ├── __init__.py          # Exporta todos agents
│   ├── router.py            # Router agent
│   ├── planner.py           # Planner agent
│   └── base.py              # Agent base classes
│
├── tasks/
│   ├── __init__.py          # Exporta todas tasks
│   ├── triage.py            # Triage tasks
│   ├── planning.py          # Planning tasks
│   └── base.py              # Task base classes
│
├── crew/
│   ├── __init__.py          # Exporta todas crews
│   ├── hello_crew.py        # Hello World crew
│   ├── ticket_crew.py       # Main ticket crew
│   └── base.py              # Crew base/factory
│
├── tools/
│   ├── __init__.py          # Exporta todas tools
│   ├── crm_api.py           # CRM integration
│   ├── kb_search.py         # Knowledge base
│   └── base.py              # Tool base classes
│
├── utils/
│   ├── env_loader.py        # Environment loading
│   ├── config.py            # Config management
│   └── helpers.py           # Utility functions
│
└── main.py                  # Entry point
```

## Padrões de Código

### Agents

```python
# src/agents/router.py
from crewai import Agent
from src.tools.search import search_tool

def create_router_agent(config: dict = None):
    """Factory function para criar router agent."""
    config = config or {}
    
    return Agent(
        role=config.get("role", "Ticket Router"),
        goal=config.get("goal", "Classify and route tickets"),
        backstory=config.get("backstory", "..."),
        tools=[search_tool],
        verbose=config.get("verbose", True),
        max_iter=config.get("max_iterations", 5),  # Reliability
        max_execution_time=config.get("timeout", 300),  # Reliability
    )
```

**Padrões:**
- ✅ Factory function (não instância direta)
- ✅ Configuração via dict (flexível)
- ✅ Valores padrão sensatos
- ✅ Reliability built-in (max_iter, timeout)

### Tasks

```python
# src/tasks/triage.py
from crewai import Task
from src.agents.router import create_router_agent
from pydantic import BaseModel

class TriageOutput(BaseModel):
    """Schema para output de triage task."""
    category: str
    priority: str
    assigned_team: str

def create_triage_task(agent, context_tasks=None):
    """Factory function para criar triage task."""
    return Task(
        description="Classify ticket: {ticket_content}",
        expected_output="JSON com category, priority, assigned_team",
        agent=agent,
        context=context_tasks or [],  # Dependencies
        output_json=TriageOutput,     # Validation (Semana 2)
    )
```

**Padrões:**
- ✅ Factory function
- ✅ Template strings com placeholders (`{ticket_content}`)
- ✅ Expected output claro
- ✅ Context para dependências
- ✅ Schema validation (quando implementado)

### Crews

```python
# src/crew/ticket_crew.py
from crewai import Crew, Process
from src.agents import create_router_agent, create_planner_agent
from src.tasks import create_triage_task, create_planning_task

def create_ticket_crew(config: dict = None):
    """Factory function para criar ticket processing crew."""
    config = config or {}
    
    # Criar agents
    router = create_router_agent(config.get("router", {}))
    planner = create_planner_agent(config.get("planner", {}))
    
    # Criar tasks (com dependências)
    triage = create_triage_task(router)
    planning = create_planning_task(planner, context=[triage])
    
    # Criar crew
    return Crew(
        agents=[router, planner],
        tasks=[triage, planning],
        process=Process.sequential,  # ou hierarchical
        verbose=config.get("verbose", True),
        max_execution_time=config.get("max_timeout", 300),
    )
```

**Padrões:**
- ✅ Factory function
- ✅ Agents criados primeiro
- ✅ Tasks criadas com dependências explícitas
- ✅ Configuração centralizada
- ✅ Reliability built-in

## Tradeoffs das Decisões

### ✅ Vantagens da Arquitetura Atual

1. **Modularidade**: Cada componente é independente e testável
2. **Escalabilidade**: Fácil adicionar novos agents/tasks/crews
3. **Testabilidade**: Factory functions são fáceis de mockar
4. **Clareza**: Imports absolutos deixam dependências explícitas
5. **Manutenibilidade**: Separação clara de responsabilidades

### ⚠️ Tradeoffs

1. **Mais arquivos**: Mais estrutura, mas mais organizado
2. **Imports mais longos**: `from src.agents.router import create_router_agent`
   - **Solução**: Usar `__init__.py` para re-exportar
3. **Factory pattern**: Mais verboso que instâncias diretas
   - **Benefício**: Mais flexibilidade e testabilidade

### 🔄 Alternativas Consideradas (e por que não usar)

1. **Tudo em um arquivo**:
   - ❌ Não escala
   - ❌ Difícil de testar
   - ❌ Violação de Single Responsibility

2. **Imports relativos em tudo**:
   - ❌ Problemas quando executado como script
   - ❌ Mais difícil de debuggar

3. **Instâncias diretas** (sem factory):
   - ❌ Código executando no import-time
   - ❌ Difícil de testar
   - ❌ Menos flexível

## Evolução Esperada

### Semana 1 (Atual)
```
hello_crew.py (básico)
  → hello_agent
  → hello_task
```

### Semana 1 (Final)
```
ticket_crew.py
  → router_agent
  → planner_agent
  → executor_agent
  → critic_agent
```

### Semana 2+
- Adicionar reliability (timeouts, retries)
- Adicionar validation (Pydantic schemas)
- Adicionar observability (logging, metrics)

### Semana 4+
- Adicionar memory/RAG
- Adicionar tools complexas

### Semana 5+
- Adicionar security layers
- Adicionar multi-tenancy
- Production-ready
