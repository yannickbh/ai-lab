"""
Environment Variable Loader

Carrega variáveis de ambiente procurando o arquivo .env em múltiplos locais:
1. Diretório atual (enterprise_ticket_assistant/)
2. Diretório pai (ai-lab/)
3. Raiz do projeto (crewai-lab/)
"""

from pathlib import Path
from dotenv import load_dotenv
import os

def load_environment():
    """
    Carrega variáveis de ambiente procurando .env em múltiplos locais.
    
    Ordem de busca:
    1. enterprise_ticket_assistant/.env
    2. ai-lab/.env
    3. crewai-lab/.env (raiz do projeto)
    """
    # Diretório atual (onde está este arquivo)
    current_dir = Path(__file__).parent.parent.parent  # enterprise_ticket_assistant/
    parent_dir = current_dir.parent  # ai-lab/
    root_dir = parent_dir.parent  # crewai-lab/
    
    # Tentar carregar de cada local (em ordem de prioridade)
    env_paths = [
        current_dir / ".env",      # enterprise_ticket_assistant/.env
        parent_dir / ".env",       # ai-lab/.env
        root_dir / ".env",         # crewai-lab/.env
    ]
    
    loaded = False
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path, override=False)  # override=False: primeiro encontrado tem prioridade
            loaded = True
            print(f"[OK] Loaded .env from: {env_path}")
            break
    
    if not loaded:
        # Fallback: tentar carregar do diretório atual do processo
        load_dotenv(override=False)
        print("[WARN] No .env found in standard locations, using current directory")
    
    return loaded


def get_env_var(key: str, default: str = None, required: bool = False) -> str:
    """
    Obtém variável de ambiente com validação.
    
    Args:
        key: Nome da variável de ambiente
        default: Valor padrão se não encontrada
        required: Se True, levanta erro se variável não existir
        
    Returns:
        Valor da variável de ambiente
        
    Raises:
        ValueError: Se required=True e variável não existe
    """
    value = os.getenv(key, default)
    
    if required and value is None:
        raise ValueError(
            f"Required environment variable '{key}' not found. "
            f"Please set it in your .env file."
        )
    
    return value


# Carregar automaticamente ao importar o módulo
load_environment()
