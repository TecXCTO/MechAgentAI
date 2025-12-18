#pip install langchain langchain-openai numpy scipy pandas coolprop sfepy

from langchain.tools import tool
import CoolProp.CoolProp as CP

@tool
def get_refrigerant_property(fluid_name: str, property_name: str, temp_celsius: float, pressure_kpa: float) -> str:
    """
    Retrieves a specific thermodynamic property for a given refrigerant at specified conditions.
    Valid property names include 'D' (density), 'H' (enthalpy), 'S' (entropy), 'T' (temperature), 'P' (pressure).
    Temperature in Celsius, Pressure in kPa.
    """
    try:
        # Convert inputs to the units CoolProp expects (e.g., K, Pa)
        temp_k = temp_celsius + 273.15
        pressure_pa = pressure_kpa * 1000
        
        # Calculate the property
        value = CP.PropsSI(property_name, "T", temp_k, "P", pressure_pa, fluid_name)
        return f"The {property_name} of {fluid_name} is: {value}"
    except Exception as e:
        return f"Error: Could not retrieve property. Check fluid name, property name, and conditions. Details: {e}"

# Example: A simple stress calculation tool using NumPy
import numpy as np

@tool
def calculate_tensile_stress(force_newtons: float, area_meters_squared: float) -> str:
    """
    Calculates the tensile stress (in Pascals) given a force in Newtons and a cross-sectional area in meters squared.
    """
    if area_meters_squared <= 0:
        return "Error: Area must be a positive value."
    stress = force_newtons / area_meters_squared
    return f"The calculated tensile stress is: {stress} Pascals."



import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

# Set your OpenAI API key as an environment variable (recommended)
# os.environ["OPENAI_API_KEY"] = "your_api_key" 

# Initialize the LLM (GPT-4 recommended for complex reasoning)
llm = ChatOpenAI(model="gpt-4", temperature=0)

# List of all available engineering tools
engineering_tools = [get_refrigerant_property, calculate_tensile_stress]

# Initialize the agent
# The 'zero-shot-react-description' agent type is good for using tools based on their descriptions
agent = initialize_agent(
    engineering_tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    handle_parsing_errors=True,
    verbose=True # Set verbose=True to see the agent's reasoning process
)

# Run the agent with a mechanical engineering task
query = "What is the tensile stress if a force of 5000 Newtons is applied over an area of 0.002 square meters?"
response = agent.run(query)
print(response)

query_thermo = "What is the density of R134a refrigerant at 25 degrees Celsius and 100 kPa pressure?"
response_thermo = agent.run(query_thermo)
print(response_thermo)
