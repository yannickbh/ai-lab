# Configuração de Variáveis de Ambiente

## 📍 Localização do .env

O projeto procura o arquivo `.env` na seguinte ordem (primeiro encontrado é usado):

1. `enterprise_ticket_assistant/.env` (específico do projeto)
2. `ai-lab/.env` (compartilhado entre projetos do ai-lab)
3. `crewai-lab/.env` (raiz do projeto - compartilhado por tudo)

## ✅ Você já tem um .env?

Se você já tem um `.env` em `ai-lab/` ou na raiz, **pode usá-lo diretamente!**

O sistema irá:
- ✅ Detectar automaticamente seu `.env` existente
- ✅ Carregar as variáveis de ambiente
- ✅ Funcionar sem necessidade de criar novo arquivo

## 🔧 Opções de Configuração

### Opção 1: Usar .env Existente (Recomendado)

Se você já tem um `.env` em `ai-lab/` com suas chaves:
- **Nada a fazer!** O sistema já vai encontrá-lo
- Apenas adicione variáveis novas se necessário (ver `env.example`)

### Opção 2: Criar .env Específico (Opcional)

Se quiser um `.env` separado para o `enterprise_ticket_assistant`:

```bash
cd ai-lab/enterprise_ticket_assistant
cp env.example .env
# Editar .env com suas chaves
```

**Nota:** O `.env` no `enterprise_ticket_assistant/` tem prioridade sobre o de `ai-lab/`.

### Opção 3: Adicionar Variáveis ao .env Existente

Se seu `.env` atual só tem `OPENAI_API_KEY`, você pode adicionar outras conforme necessário:

```bash
# Editar seu .env existente (em ai-lab/ ou raiz)
# Adicionar apenas as variáveis que vai usar:

# Mínimo para começar (Semana 1):
OPENAI_API_KEY=your_existing_key

# Opcional para Semana 1-2 (se usar busca web):
SERPER_API_KEY=your_key_here

# Semana 4 (RAG):
QDRANT_URL=http://localhost:6333

# Semana 5 (Observability):
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
PROMETHEUS_PORT=8000
```

## 🔍 Verificar se .env está sendo Carregado

Execute este comando para verificar:

```python
python -c "from src.utils.env_loader import load_environment, get_env_var; import os; load_environment(); print('OPENAI_API_KEY:', '✓ Found' if os.getenv('OPENAI_API_KEY') else '✗ Not found')"
```

Ou use o helper:

```python
from src.utils.env_loader import get_env_var

# Verificar se variável existe
api_key = get_env_var("OPENAI_API_KEY")
if api_key:
    print("✓ OPENAI_API_KEY encontrada")
else:
    print("✗ OPENAI_API_KEY não encontrada")
```

## 📝 Variáveis Necessárias por Fase

### Semana 1 (Fundações CrewAI)
- `OPENAI_API_KEY` - **Obrigatória**

### Semana 1-2 (Tools)
- `OPENAI_API_KEY` - **Obrigatória**
- `SERPER_API_KEY` - Opcional (para busca web)

### Semana 4 (RAG)
- `OPENAI_API_KEY` - **Obrigatória**
- `QDRANT_URL` - Opcional (padrão: http://localhost:6333)

### Semana 5 (Observability)
- `OPENAI_API_KEY` - **Obrigatória**
- `OTEL_EXPORTER_OTLP_ENDPOINT` - Opcional
- `PROMETHEUS_PORT` - Opcional (padrão: 8000)

## 🛡️ Segurança

- ✅ `.env` já está no `.gitignore` (não será commitado)
- ✅ Nunca commite chaves de API
- ✅ Use `.env.example` como template para documentação

## ❓ Troubleshooting

### Erro: "Required environment variable 'OPENAI_API_KEY' not found"

**Solução:**
1. Verifique se o `.env` existe em um dos locais mencionados
2. Verifique se `OPENAI_API_KEY` está definida no `.env`
3. Execute: `python -c "from src.utils.env_loader import load_environment; load_environment()"`

### Quer usar um .env diferente?

Você pode especificar o caminho manualmente:

```python
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path("/caminho/para/seu/.env"))
```

### Verificar de onde o .env foi carregado

O sistema imprime no console qual `.env` foi carregado:
```
✓ Loaded .env from: C:\Users\yanni\Yan-projects\crewai-lab\ai-lab\.env
```

---

## ✅ Checklist

- [ ] Verificar se `.env` existe em `ai-lab/` ou raiz
- [ ] Confirmar que `OPENAI_API_KEY` está configurada
- [ ] Testar carregamento: `python -c "from src.utils.env_loader import load_environment; load_environment()"`
- [ ] (Opcional) Adicionar variáveis adicionais conforme necessário
