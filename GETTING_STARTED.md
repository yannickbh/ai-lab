# Getting Started: Enterprise Ticket Assistant

Guia rápido para começar o projeto de referência e seguir o plano de 30 dias.

---

## 📋 Pré-requisitos

- Python 3.10+
- pip ou poetry
- Git
- (Opcional) Docker para serviços (Qdrant, PostgreSQL)

---

## 🚀 Setup Inicial (Dia 1)

### 1. Criar Ambiente Virtual

```bash
cd ai-lab/enterprise_ticket_assistant
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt

# Ou com pip-tools (recomendado para desenvolvimento)
pip install pip-tools
pip-compile requirements.in  # Criar requirements.in se necessário
pip-sync requirements.txt
```

### 3. Configurar Variáveis de Ambiente

**Você já tem um .env?** Se sim, pode usá-lo diretamente! O sistema procura em:
1. `enterprise_ticket_assistant/.env`
2. `ai-lab/.env` ← **Seu .env existente será usado aqui**
3. `crewai-lab/.env` (raiz)

**Opção A: Usar .env Existente (Recomendado)**
```bash
# Se já tem .env em ai-lab/, apenas adicione OPENAI_API_KEY se não tiver
# Nada mais a fazer!
```

**Opção B: Criar .env Específico (Opcional)**
```bash
# Se quiser um .env separado para este projeto:
cp env.example .env

# Editar .env com suas chaves de API
# Mínimo necessário para começar:
# - OPENAI_API_KEY
# - (Opcional) SERPER_API_KEY para busca web
```

**Verificar se está configurado:**
```bash
python scripts/check_env.py
```

Veja [docs/ENV_SETUP.md](enterprise_ticket_assistant/docs/ENV_SETUP.md) para mais detalhes.

### 4. Verificar Instalação

```bash
python -c "import crewai; print(f'CrewAI version: {crewai.__version__}')"
python -m pytest tests/unit/test_agents.py -v  # Se houver testes básicos
```

---

## 📚 Estrutura do Projeto

```
enterprise_ticket_assistant/
├── src/
│   ├── agents/           # ✅ Semana 1: Definir agents aqui
│   ├── tasks/            # ✅ Semana 1: Definir tasks aqui
│   ├── tools/            # ✅ Semana 1-2: Criar tools aqui
│   ├── crew/             # ✅ Semana 1: Criar crew aqui
│   ├── memory/           # ✅ Semana 4: Memory management
│   ├── rag/              # ✅ Semana 4: RAG pipeline
│   ├── security/         # ✅ Semana 5: PII handling
│   ├── observability/    # ✅ Semana 5: Logging, metrics
│   ├── reliability/      # ✅ Semana 2-3: Retries, timeouts
│   └── utils/            # Helpers
├── tests/
│   ├── unit/             # ✅ Semana 1: Testes unitários
│   ├── integration/      # ✅ Semana 3: Testes de integração
│   └── evaluation/       # ✅ Semana 5: Evaluation harness
├── mocks/                # ✅ Semana 3: Mock APIs
├── config/               # ✅ Configuração YAML
├── docs/                 # ✅ Documentação (debug, evaluation)
└── scripts/              # ✅ Scripts utilitários
```

---

## 📅 Plano de 30 Dias - Quick Reference

### **Semana 1 (Dias 1-7): Fundações CrewAI**
- ✅ Dia 1-2: Setup + Hello World
- ✅ Dia 3-4: Tools & Tool Calling
- ✅ Dia 5-6: Multi-Agent Workflows
- ✅ Dia 7: Review + Testes

**Checkpoint Semana 1:** Multi-agent crew funcional com workflow básico

### **Semana 2 (Dias 8-14): Reliability**
- ✅ Dia 8-9: Emergent Failures (loops, timeouts)
- ✅ Dia 10-11: Determinism & Validation
- ✅ Dia 12-13: Async & Concurrency
- ✅ Dia 14: Review + Stress Testing

**Checkpoint Semana 2:** Sistema robusto contra falhas comuns

### **Semana 3 (Dias 15-21): Integrations**
- ✅ Dia 15-16: Retries & Idempotency
- ✅ Dia 17-18: Rate Limiting
- ✅ Dia 19-20: Secure Integrations
- ✅ Dia 21: Review + Integration Testing

**Checkpoint Semana 3:** Integrações robustas e seguras

### **Semana 4 (Dias 22-28): Memory & RAG**
- ✅ Dia 22-23: Memory & Context Windows
- ✅ Dia 24-25: RAG Pipeline Básico
- ✅ Dia 26-27: Integration RAG + CrewAI
- ✅ Dia 28: Review + RAG Evaluation

**Checkpoint Semana 4:** Sistema com memória e RAG funcional

### **Semana 5 (Dias 29-30): Enterprise Ready**
- ✅ Dia 29: Security & Guardrails
- ✅ Dia 30: Observability & Governance

**Checkpoint Final:** Sistema enterprise-ready completo

---

## 🎯 Primeiros Passos - Dia 1

### 1. Criar Hello World CrewAI

Criar arquivo: `src/agents/basic_agent.py`

```python
from crewai import Agent

def create_basic_agent():
    """Criar agente básico para teste inicial."""
    return Agent(
        role="Assistant",
        goal="Say hello and test CrewAI setup",
        backstory="You are a helpful assistant testing the CrewAI framework",
        verbose=True
    )
```

Criar arquivo: `src/tasks/basic_task.py`

```python
from crewai import Task

def create_hello_task(agent):
    """Criar task básica para teste inicial."""
    return Task(
        description="Say 'Hello, CrewAI!' and confirm the setup is working",
        expected_output="A greeting message confirming CrewAI is working",
        agent=agent
    )
```

Criar arquivo: `src/crew/basic_crew.py`

```python
from crewai import Crew
from src.agents.basic_agent import create_basic_agent
from src.tasks.basic_task import create_hello_task

def create_basic_crew():
    """Criar crew básico para teste inicial."""
    agent = create_basic_agent()
    task = create_hello_task(agent)
    
    return Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
```

Criar arquivo: `scripts/test_hello.py`

```python
"""Script de teste inicial do CrewAI."""
from src.crew.basic_crew import create_basic_crew

if __name__ == "__main__":
    crew = create_basic_crew()
    result = crew.kickoff()
    print(f"\nResult: {result}\n")
```

### 2. Executar Teste

```bash
python scripts/test_hello.py
```

**Validação:** Deve executar sem erros e retornar uma mensagem de saudação.

---

## 📖 Próximos Passos

1. **Dia 1-2:** Completar Hello World e entender Agent/Task/Crew
2. **Dia 3:** Começar a criar tools customizadas
3. **Seguir o plano:** Ver [STUDY_PLAN.md](../STUDY_PLAN.md) para detalhes dia a dia

---

## 🐛 Troubleshooting Inicial

### Erro: `ImportError: cannot import name 'Agent' from 'crewai'`

**Solução:**
```bash
pip install --upgrade crewai
```

### Erro: `OPENAI_API_KEY not found`

**Solução:**
```bash
# Verificar se .env existe
ls -la .env

# Verificar se variável está carregada
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY'))"
```

### Erro: `ModuleNotFoundError`

**Solução:**
```bash
# Instalar dependências faltantes
pip install -r requirements.txt

# Verificar se está no ambiente virtual correto
which python  # Linux/Mac
where python  # Windows
```

---

## 📚 Recursos Adicionais

- **Plano Completo:** [STUDY_PLAN.md](../STUDY_PLAN.md)
- **Debug Playbook:** [docs/debug_playbook.md](docs/debug_playbook.md)
- **Evaluation Guide:** [docs/evaluation.md](docs/evaluation.md)
- **CrewAI Docs:** https://docs.crewai.com
- **Projeto README:** [README.md](README.md)

---

## ✅ Checklist de Início

Antes de começar o Dia 1, confirme:

- [ ] Python 3.10+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` configurado com `OPENAI_API_KEY`
- [ ] Teste Hello World executado com sucesso
- [ ] Estrutura de diretórios criada
- [ ] README e documentação lidos

---

## 🎓 Perguntas Frequentes

**Q: Posso pular dias ou semanas?**  
A: Não recomendado. Cada semana constrói sobre a anterior. Se já souber algo, use como revisão rápida.

**Q: E se ficar travado em algo?**  
A: Consulte o [Debug Playbook](docs/debug_playbook.md) e os logs estruturados. Debug sem UI é parte do aprendizado.

**Q: Preciso de todas as ferramentas (Qdrant, Prometheus, etc.) desde o início?**  
A: Não. Use mocks inicialmente. Semana 4+ para RAG, Semana 5 para observability completa.

**Q: Posso usar outro LLM além de OpenAI?**  
A: Sim. CrewAI suporta múltiplos providers. Ajuste `.env` e configure conforme necessário.

---

Boa sorte com sua jornada! 🚀
