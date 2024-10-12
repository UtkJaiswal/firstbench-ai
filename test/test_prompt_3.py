import instructor
from utils.object import *
from utils.jinja import *
from openai import OpenAI
from langchain_openai import ChatOpenAI
import jinja2
from langsmith import traceable
import json  
from utils.env import *

@traceable
def test(response_class, temp_name: str, **kwargs) -> str:
    llm = ChatOpenAI(temperature=1, model="gpt-3.5-turbo")

    try:
        # Using Jinja2 to render the prompt from the template
        prompt = PromptManager.get_prompt(temp_name, **kwargs)

        # Invoke the OpenAI model using the rendered prompt
        response = llm.invoke(prompt)
        
        # Parse the response content as JSON
        try:
            response_data = json.loads(response.content)
        except json.JSONDecodeError:
            # Handle the case where the response is not valid JSON
            return json.dumps({
                "error": "Invalid JSON response from the model."
            })

        # Safely access the response data if parsing is successful
        response_json = {
            "overall": response_data.get("overall", "No overall feedback available."),
            "Suggestions": response_data.get("suggestions", [])
        }
        return json.dumps(response_json)

    except Exception as e:
        # Handle any other exceptions and return an error message in JSON format
        error_response = {
            "error": str(e)
        }
        return json.dumps(error_response)

if __name__ == "__main__":
    # Sample usage
    from pydantic import BaseModel
    from typing import List
    setup_environment()

    # Pydantic Response Class definition
    class ResponseClass(BaseModel):
        argument_type: str
        topic_category: str
        dynamic_metrics: List[str]

    # Define a sample template name and any necessary keyword arguments
    template_name = "third"  # Replace with your actual template name

    # Example kwargs (now correctly formatted)
    kwargs_example = {
        "argument": "AI can improve diagnostic accuracy and patient care.",
        "deductions": {
            "Clarity and Structure": "The introduction lacks a clear thesis statement.",
            "Use of Evidence": "No quantitative data provided to support claims about economic impact.",
            "Persuasiveness": "The argument does not address potential counterarguments."
        }
    }

    # Call the test function
    json_output = test(ResponseClass, template_name, **kwargs_example)

    # Print the resulting output
    print(f"Output: \n{json_output}")