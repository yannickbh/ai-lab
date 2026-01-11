"""Hello World script para testar setup básico do CrewAI."""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports absolutos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from src.utils.env_loader import load_environment
from src.crew.crew import create_hello_crew

# Carregar variáveis de ambiente
load_environment()

if __name__ == "__main__":
    print("=" * 60)
    print("Hello World - CrewAI Test")
    print("=" * 60)
    print()
    
    # Criar e executar crew
    crew = create_hello_crew()
    result = crew.kickoff()
    
    print()
    print("=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(result)