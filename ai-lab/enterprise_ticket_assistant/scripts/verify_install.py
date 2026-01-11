"""Script para verificar se todas as dependências foram instaladas corretamente."""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_imports():
    """Verifica se todos os imports principais funcionam."""
    results = []
    
    # CrewAI Core
    try:
        import crewai
        results.append(("OK", "crewai", crewai.__version__))
    except ImportError as e:
        results.append(("FAIL", "crewai", f"Error: {e}"))
    
    try:
        import crewai_tools
        results.append(("OK", "crewai-tools", "installed"))
    except ImportError as e:
        results.append(("FAIL", "crewai-tools", f"Error: {e}"))
    
    # Reliability
    try:
        import tenacity
        results.append(("OK", "tenacity", "installed"))
    except ImportError as e:
        results.append(("FAIL", "tenacity", f"Error: {e}"))
    
    try:
        import aiolimiter
        results.append(("OK", "aiolimiter", "installed"))
    except ImportError as e:
        results.append(("FAIL", "aiolimiter", f"Error: {e}"))
    
    # HTTP
    try:
        import httpx
        results.append(("OK", "httpx", httpx.__version__))
    except ImportError as e:
        results.append(("FAIL", "httpx", f"Error: {e}"))
    
    # RAG
    try:
        import sentence_transformers
        results.append(("OK", "sentence-transformers", "installed"))
    except ImportError as e:
        results.append(("FAIL", "sentence-transformers", f"Error: {e}"))
    
    try:
        from qdrant_client import QdrantClient
        results.append(("OK", "qdrant-client", "installed"))
    except ImportError as e:
        results.append(("FAIL", "qdrant-client", f"Error: {e}"))
    
    # Observability
    try:
        import structlog
        results.append(("OK", "structlog", "installed"))
    except ImportError as e:
        results.append(("FAIL", "structlog", f"Error: {e}"))
    
    try:
        from opentelemetry import trace
        results.append(("OK", "opentelemetry", "installed"))
    except ImportError as e:
        results.append(("FAIL", "opentelemetry", f"Error: {e}"))
    
    try:
        from prometheus_client import Counter
        results.append(("OK", "prometheus-client", "installed"))
    except ImportError as e:
        results.append(("FAIL", "prometheus-client", f"Error: {e}"))
    
    # Security & Validation
    try:
        import pydantic
        results.append(("OK", "pydantic", pydantic.__version__))
    except ImportError as e:
        results.append(("FAIL", "pydantic", f"Error: {e}"))
    
    try:
        from dotenv import load_dotenv
        results.append(("OK", "python-dotenv", "installed"))
    except ImportError as e:
        results.append(("FAIL", "python-dotenv", f"Error: {e}"))
    
    # Testing
    try:
        import pytest
        results.append(("OK", "pytest", pytest.__version__))
    except ImportError as e:
        results.append(("FAIL", "pytest", f"Error: {e}"))
    
    try:
        import respx
        results.append(("OK", "respx", "installed"))
    except ImportError as e:
        results.append(("FAIL", "respx", f"Error: {e}"))
    
    # Utilities
    try:
        import rich
        results.append(("OK", "rich", "installed"))
    except ImportError as e:
        results.append(("FAIL", "rich", f"Error: {e}"))
    
    return results


def main():
    """Executa verificação de instalação."""
    print("=" * 60)
    print("Verificando Instalação de Dependências")
    print("=" * 60)
    print()
    
    results = check_imports()
    
    # Exibir resultados
    for status, package, info in results:
        print(f"[{status:4}] {package:25} {info}")
    
    print()
    print("-" * 60)
    
    # Contar sucessos e falhas
    success = sum(1 for s, _, _ in results if s == "OK")
    total = len(results)
    
    print(f"Resultado: {success}/{total} pacotes instalados corretamente")
    
    # Testar env loader
    print()
    print("Testando Environment Loader:")
    print("-" * 60)
    try:
        from src.utils.env_loader import load_environment
        load_environment()
        print("[OK  ] Environment loader funcionando")
    except Exception as e:
        print(f"[FAIL] Environment loader erro: {e}")
    
    print()
    print("=" * 60)
    
    if success == total:
        print("[OK  ] Todas as dependencias instaladas com sucesso!")
        return 0
    else:
        print("[WARN] Algumas dependencias nao foram instaladas corretamente")
        return 1


if __name__ == "__main__":
    sys.exit(main())
