"""
Enterprise Ticket Assistant - Main Entry Point

Usage:
    python -m src.main --ticket-id 12345
    python -m src.main --ticket-id 12345 --tenant-id acme-corp
"""

import argparse
import asyncio
from pathlib import Path

# Load environment variables (procura .env em múltiplos locais)
from src.utils.env_loader import load_environment, get_env_var

# Carregar variáveis de ambiente
load_environment()

# TODO: Import crew and agents as we build them
# from src.crew.ticket_crew import create_ticket_crew
# from src.observability.logging import setup_logging


async def main(ticket_id: str, tenant_id: str = "default"):
    """
    Main entry point for processing a ticket.
    
    Args:
        ticket_id: ID of the ticket to process
        tenant_id: Tenant identifier for isolation
    """
    # Setup logging
    # logger = setup_logging()
    # logger.info("Starting ticket processing", ticket_id=ticket_id, tenant_id=tenant_id)
    
    print(f"Processing ticket {ticket_id} for tenant {tenant_id}")
    
    # TODO: Week 1 - Create basic crew
    # crew = create_ticket_crew()
    # result = await crew.kickoff(inputs={"ticket_id": ticket_id, "tenant_id": tenant_id})
    # print(f"Result: {result}")
    
    # Placeholder for now
    return {"status": "not_implemented", "ticket_id": ticket_id}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise Ticket Assistant")
    parser.add_argument("--ticket-id", required=True, help="Ticket ID to process")
    parser.add_argument("--tenant-id", default="default", help="Tenant ID")
    
    args = parser.parse_args()
    
    # Run async main
    result = asyncio.run(main(args.ticket_id, args.tenant_id))
    print(result)
