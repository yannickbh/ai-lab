from crewai import Crew, Process
from src.agents.agents import hello_agent
from src.tasks.tasks import hello_task

def create_hello_crew():
    """Cria um crew básico para teste Hello World."""
    return Crew(
        agents=[hello_agent],
        tasks=[hello_task],
        process=Process.sequential,
        verbose=True
    )