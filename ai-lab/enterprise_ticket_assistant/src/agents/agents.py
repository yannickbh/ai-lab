from crewai import Agent

hello_agent = Agent(
    role="HelloWorld",
    goal="Say hello and test CrewAI setup",
    backstory="You are a helpful assistant testing the CrewAI framework",
    verbose=True
)