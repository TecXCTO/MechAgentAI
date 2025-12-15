#pip install google-genai numpy scipy python-dotenv

import numpy as np
from google.genai import types

def calculate_yield_strength(material_type: str, temperature_celsius: float) -> str:
    """
    Calculates the approximate yield strength (MPa) for common engineering materials at a given temperature.
    
    Args:
        material_type: The type of material (e.g., 'steel', 'aluminum').
        temperature_celsius: The temperature in degrees Celsius.
        
    Returns:
        A string describing the approximate yield strength or an error message.
    """
    if material_type.lower() == 'steel':
        # Placeholder for real data/model
        strength = 250 - (temperature_celsius * 0.5) 
        return f"Approximate yield strength for steel at {temperature_celsius}°C is {strength} MPa."
    elif material_type.lower() == 'aluminum':
        # Placeholder for real data/model
        strength = 70 - (temperature_celsius * 0.2)
        return f"Approximate yield strength for aluminum at {temperature_celsius}°C is {strength} MPa."
    else:
        return f"Error: Material type '{material_type}' not recognized."

def perform_stress_analysis(force_newtons: float, cross_sectional_area_m2: float) -> str:
    """
    Performs a basic stress analysis (Pa) given force (N) and area (m^2).

    Args:
        force_newtons: The applied force in Newtons.
        cross_sectional_area_m2: The cross-sectional area in square meters.

    Returns:
        A string indicating the calculated stress value.
    """
    try:
        stress = force_newtons / cross_sectional_area_m2
        return f"The calculated stress is {stress} Pascals (Pa)."
    except ZeroDivisionError:
        return "Error: Area cannot be zero."



import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Map tool names to actual function implementations
available_tools = {
    'calculate_yield_strength': calculate_yield_strength,
    'perform_stress_analysis': perform_stress_analysis
}

# Define the Tool for the Gemini API using automatic schema generation from functions
# Note: This is simpler than manual JSON schema creation
engineering_tools = types.Tool.from_functions(list(available_tools.values()))

def run_engineering_agent(prompt: str):
    client = genai.Client(api_key=API_KEY)
    model = "gemini-2.5-flash" # Use a model that supports function calling

    # First turn: Send the user prompt and available tools to the model
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(tools=[engineering_tools])
    )

    # Check if the model decided to call a function
    if response.function_calls:
        for call in response.function_calls:
            tool_name = call.name
            tool_args = dict(call.args)
            print(f"[Agent calling tool: {tool_name} with args {tool_args}]")
            
            # Execute the function in your application code
            function_response_content = available_tools[tool_name](**tool_args)
            print(f"[Tool response: {function_response_content}]")

            # Second turn: Send the function response back to the model
            # The model uses this result to formulate a natural language answer
            second_response = client.models.generate_content(
                model=model,
                contents=[
                    {"role": "user", "parts": [{"text": prompt}]},
                    {"role": "function", "parts": [{"text": function_response_content}]}
                ],
                config=types.GenerateContentConfig(tools=[engineering_tools]) # Tools still available
            )
            return second_response.text
    else:
        # If no tool call was made, the model responded directly
        return response.text

# --- Example Usage ---
user_query = "What is the yield strength for steel at 20 degrees Celsius? And what is the stress if I apply a force of 5000 N over an area of 0.01 square meters?"

result = run_engineering_agent(user_query)
print("\n--- Final Agent Response ---")
print(result)
