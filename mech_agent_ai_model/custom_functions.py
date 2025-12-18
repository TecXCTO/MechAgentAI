# In custom_functions.py
def get_fx_rate(base: str, target: str) -> dict:
    """Fetches the current exchange rate between two currencies."""
    # ... implementation details ...
    return {"rate": 10.0}

# In agent.py
##from .custom_functions import get_fx_rate  # Relative import
##from google.adk.agents.llm_agent import Agent

##root_agent = Agent(
    # ... other parameters ...
    ##tools=[get_fx_rate],
##)

