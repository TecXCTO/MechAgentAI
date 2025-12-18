
# In agent.py
from .custom_functions import get_fx_rate  # Relative import
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    # ... other parameters ...
    tools=[get_fx_rate],
)
