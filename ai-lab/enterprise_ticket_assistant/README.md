# Enterprise Ticket Assistant

Sistema multi-agente CrewAI para triagem, análise e resolução automatizada de tickets de suporte.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Enterprise Ticket Assistant                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐   ┌─────────┐│
│  │  Router  │───▶│ Planner  │───▶│ Executor │──▶│ Critic  ││
│  │  Agent   │    │  Agent   │    │  Agent   │   │  Agent  ││
│  └──────────┘    └──────────┘    └──────────┘   └─────────┘│
│       │               │               │              │       │
│       ▼               ▼               ▼              ▼       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Tools Layer                           ││
│  │  • CRM API      • KB Search    • RAG Retrieval          ││
│  │  • Ticket DB    • Email Send   • Document Parser        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Infrastructure Layer                        ││
│  │  • Memory (SQLite/PG)   • Vector DB (Qdrant)           ││
│  │  • Observability (OTEL)  • Metrics (Prometheus)        ││
│  │  • Security (PII Mask)   • Reliability (Retries)       ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Componentes

### Agents
- **Router**: Triage inicial, classificação de tickets
- **Planner**: Cria plano de resolução baseado em histórico
- **Executor**: Executa ações via APIs (CRM, email, KB)
- **Critic**: Revisa qualidade e valida outputs

### Tools
- CRM API integration (mock)
- Knowledge Base search
- RAG retrieval para histórico
- Email sending
- Document parsing

### Infrastructure
- Memory management (SQLite/PostgreSQL)
- Vector store (Qdrant) para RAG
- Observability (structlog + OpenTelemetry)
- Metrics (Prometheus)
- Security (PII redaction, tenant isolation)
- Reliability (retries, timeouts, circuit breakers)

## Estrutura do Projeto

```
enterprise_ticket_assistant/
├── src/
│   ├── agents/           # Agent definitions
│   ├── tasks/            # Task definitions
│   ├── tools/            # Custom tools
│   ├── crew/             # Crew orchestration
│   ├── memory/           # Memory management
│   ├── rag/              # RAG pipeline
│   ├── security/         # PII handling, tenant isolation
│   ├── observability/    # Logging, tracing, metrics
│   ├── reliability/      # Retries, timeouts, circuit breakers
│   └── utils/            # Helpers
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── evaluation/       # Evaluation harness
├── mocks/                # Mock APIs for testing
├── config/               # Configuration files
├── docs/                 # Documentation
│   ├── debug_playbook.md
│   └── evaluation.md
└── scripts/              # Utility scripts
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run basic test
python -m pytest tests/unit/test_agents.py -v

# Run the assistant
python -m src.main --ticket-id 12345
```

## Próximos Passos

Veja [STUDY_PLAN.md](../../STUDY_PLAN.md) para o plano de 30 dias detalhado.
