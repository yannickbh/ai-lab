from crewai import Task
from src.agents.agents import hello_agent

hello_task = Task(
    description="Say 'Hello, CrewAI!' and confirm the setup is working",
    expected_output="A greeting message confirming CrewAI is working",
    agent=hello_agent
)