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

def argument_genre(pydentic_class, prompt_temp_name: str, **kwargs) -> str:
    """
    Tests the OpenAI model with a given template and arguments, returning the response in JSON format.

    Parameters:
    - pydentic_class: A Pydantic model specifying the response class.
    - prompt_temp_name: The name of the template to be used for the prompt.
    - kwargs: Additional arguments for the prompt rendering.

    Returns:
    - A JSON string containing the model response.
    """
    llm = ChatOpenAI(temperature=1, model="gpt-3.5-turbo")
    
    try:
        # Using Jinja2 to render the prompt from the template
        prompt = PromptManager.get_prompt(prompt_temp_name, **kwargs)
        # Debug: Print the rendered prompt
        response = llm.invoke(prompt)
        # Debug: Print the model response
        response_text = response.content
        
        # Parse the response assuming it's a JSON string
        response_data = json.loads(response_text)

        # Extract the necessary fields from the response
        dynamic_metrics = response_data.get("dynamic_metrics", [])
        
        # Reformat the response to match the expected structure
        reformatted_response = {
            "genre_metrics": [
                {
                    "genre": genre_data.get("genre"),
                    "dynamic_metric": [
                        {
                            "metric": metric.get("metric"),
                            "relevance_score": metric.get("relevance_score")
                        } for metric in genre_data.get("dynamic_metric", [])
                    ]
                } for genre_data in dynamic_metrics
            ]
        }

        return json.dumps(reformatted_response, indent=2)  # Return the response as a JSON string, formatted nicely

    except Exception as e:
        # Handle any exceptions and return an error message in JSON format
        error_response = {
            "error!!": str(e)
        }
        return json.dumps(error_response)


if __name__ == "__main__":
    # Sample usage
    from pydantic import BaseModel
    from typing import List
    import pprint
    
    setup_environment()
  
    prompt_temp_name ="first"  
    
    kwargs_example = {
        "question": "Should AI be used in healthcare?",
        "user_argument": """AI should be used in healthcare because it can help diagnose diseases more accurately and quickly.
                            By analyzing large amounts of data, AI can identify patterns that humans might miss.
                            This can lead to faster treatment and better outcomes for patients. 
                            Additionally, AI can help personalize treatment plans based on individual patient data,
                            leading to more effective care. Overall, AI has the potential to revolutionize healthcare
                            and improve patient outcomes. On the other hand, some people are concerned about privacy
                            and data security when it comes to using AI in healthcare. There are also ethical
                            considerations to take into account, such as the potential for bias in AI algorithms.
                            However, with proper regulations and oversight, AI can be used responsibly in healthcare
                            to benefit patients and providers.
        """
    }

    # Call the test function
    json_output = argument_genre(FirstPromptClass, prompt_temp_name, **kwargs_example)
    # Print the JSON output
    print(json_output)
    