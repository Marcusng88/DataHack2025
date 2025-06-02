from google.adk.agents import Agent
from .prompts import return_instruction_root
from google.adk.tools import load_artifacts, google_search

root_agent = Agent(
    name="ds_agent",
    model="gemini-2.0-flash",
    instruction=return_instruction_root(),
    global_instruction="You are a data science and ecosystem insights multiagent system who gives insights on SDG topics (Life Under Water) based on a dataset",
    tools=[
        load_artifacts,
    ]
)