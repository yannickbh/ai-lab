"""
Script para verificar se as variáveis de ambiente estão sendo carregadas corretamente.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.env_loader import load_environment, get_env_var
import os

def main():
    """Verifica se as variáveis de ambiente necessárias estão configuradas."""
    print("=" * 60)
    print("Verificando Configuração de Variáveis de Ambiente")
    print("=" * 60)
    print()
    
    # Carregar ambiente
    load_environment()
    print()
    
    # Lista de variáveis para verificar
    required_vars = {
        "OPENAI_API_KEY": True,  # Obrigatória
        "SERPER_API_KEY": False,  # Opcional
        "QDRANT_URL": False,      # Opcional
        "DATABASE_URL": False,    # Opcional
    }
    
    print("Status das Variáveis:")
    print("-" * 60)
    
    all_ok = True
    for var_name, required in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # Mascarar chaves sensíveis
            if "KEY" in var_name or "SECRET" in var_name:
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            else:
                display_value = value
            
            status = "✓" if required else "•"
            print(f"{status} {var_name:25} = {display_value}")
        else:
            if required:
                print(f"✗ {var_name:25} = NOT FOUND (OBRIGATÓRIA)")
                all_ok = False
            else:
                print(f"○ {var_name:25} = não configurada (opcional)")
    
    print()
    print("-" * 60)
    
    # Verificar local do .env
    env_paths = [
        Path(__file__).parent.parent / ".env",           # enterprise_ticket_assistant/.env
        Path(__file__).parent.parent.parent / ".env",    # ai-lab/.env
        Path(__file__).parent.parent.parent.parent / ".env",  # crewai-lab/.env
    ]
    
    print("\nLocais verificados para .env:")
    for env_path in env_paths:
        if env_path.exists():
            print(f"  ✓ {env_path} (ENCONTRADO)")
        else:
            print(f"  ○ {env_path} (não encontrado)")
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✓ Configuração OK! Você pode começar a trabalhar.")
        return 0
    else:
        print("✗ Configuração incompleta. Por favor, configure as variáveis obrigatórias.")
        print("\nDica: Edite seu .env existente ou crie um novo baseado em env.example")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
