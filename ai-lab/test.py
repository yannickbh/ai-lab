from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, Process

agent = Agent(role="Tester", goal="Say Hello", backstory="Just testing CrewAI.")
task = Task(description="Say hello world", expected_output="Hello World!", agent=agent)
crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)

print(crew.kickoff())