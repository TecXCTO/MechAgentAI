#pip install google-genai numpy cadquery build123d python-dotenv
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import build123d as b3d # Library for programmatic CAD

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# --- Define the CAD Tool (Function) ---
def create_parametric_box_with_hole(length: float, width: float, height: float, hole_diameter: float, filename: str = "output_model.step") -> str:
    """
    Generates a 3D CAD model of a box with a central hole using build123d.
    The model is saved as a STEP file, a standard format for mechanical engineering.

    Args:
        length: The length of the box in mm.
        width: The width of the box in mm.
        height: The height of the box in mm.
        hole_diameter: The diameter of the central hole in mm.
        filename: The output filename (default: output_model.step).

    Returns:
        A status string indicating the file path of the generated 3D model.
    """
    with b3d.BuildPart() as part:
        b3d.Box(length, width, height)
        b3d.Workplane(part.faces().sort_by(b3d.Axis.Z)[-1]).hole(hole_diameter) # Top face hole
    
    # Export the model to a STEP file
    b3d.export_step(part.part, filename)
    return f"Successfully created 3D model: {os.path.abspath(filename)}"

# Map the tool function for the agent
available_tools = {
    'create_parametric_box_with_hole': create_parametric_box_with_hole
}
engineering_tools = types.Tool.from_functions(list(available_tools.values()))

# --- Agent Orchestration Logic ---
def run_3d_modeling_agent(prompt: str):
    client = genai.Client(api_key=API_KEY)
    model = "gemini-2.5-flash"

    # Send the user prompt and available tools to the model (Turn 1)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(tools=[engineering_tools])
    )

    # Check for and execute function calls
    if response.function_calls:
        for call in response.function_calls:
            tool_name = call.name
            tool_args = dict(call.args)
            print(f"[Agent calling tool: {tool_name} with args {tool_args}]")
            
            # Execute the function
            function_response_content = available_tools[tool_name](**tool_args)
            print(f"[Tool response: {function_response_content}]")

            # Send function response back to the model (Turn 2)
            second_response = client.models.generate_content(
                model=model,
                contents=[
                    {"role": "user", "parts": [{"text": prompt}]},
                    {"role": "function", "parts": [{"text": function_response_content}]}
                ],
                config=types.GenerateContentConfig(tools=[engineering_tools])
            )
            return second_response.text
    else:
        # If no tool was called, return the direct response
        return response.text

# --- Example Usage ---
user_query = "Design a basic mechanical part: a box that is 100mm long, 50mm wide, and 30mm high. It needs a central hole with a 15mm diameter. Save the model as final_design.step."

result = run_3d_modeling_agent(user_query)
print("\n--- Final Agent Response ---")
print(result)



