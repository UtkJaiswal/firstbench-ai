import instructor
from utils.object import *
from utils.jinja import *
from openai import OpenAI
from langchain_openai import ChatOpenAI
import jinja2
from langsmith import traceable
import json
from utils.env import *
from pydantic import BaseModel
from typing import List
@traceable
def generate_complex_question(pydentic_class, prompt_temp_name: str, **kwargs) -> str:
    """
    Generates a complex UPSC question using a given template and arguments, returning the response in JSON format.
    """
    llm = ChatOpenAI(temperature=1, model="gpt-3.5-turbo")
    try:
        # Using Jinja2 to render the prompt from the template
        prompt = PromptManager.get_prompt(prompt_temp_name, **kwargs)
        
        # Debug: Print the rendered prompt
    
        
        # Invoke the LLM
        response = llm.invoke(prompt)
        
        # Debug: Print the raw response
        
        # Parse the response assuming it's a JSON string
        try:
            response_data = json.loads(response.content)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {str(e)}")
            return json.dumps({"error": "Invalid JSON response", "content": response.content})
        
        # Return the response as a JSON string, formatted nicely
        return json.dumps(response_data, indent=2)
    
    except Exception as e:
        # Handle any exceptions and return an error message in JSON format
        error_response = {
            "error": str(e)
        }
        return json.dumps(error_response)


if __name__ == "__main__":
    # Set up the environment
    setup_environment()
    
    # Define the template name
    prompt_temp_name = "q_gen"
    
    # Sample kwargs for the question generation (only subject, topic, subtopic)
    kwargs_example = {
        "subject": "Political Science",
        "topic": "International Relations",
        "subtopic": "Global Governance"
    }
    
    # Call the generate_complex_question function
    json_output = generate_complex_question(BaseModel, prompt_temp_name, **kwargs_example)
    
    # Print the JSON output
    print(json_output)
