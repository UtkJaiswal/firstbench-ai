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
def generate_explanation(pydentic_class, prompt_temp_name: str, **kwargs) -> str:
    """
    Tests the OpenAI model with a given template and arguments, returning the response in JSON format.

    Parameters:
    - pydentic_class: A Pydantic model specifying the response class.
    - prompt_temp_name: The name of the template to be used for the prompt.
    - kwargs: Additional arguments for the prompt rendering (e.g., question, user argument, reasons for deduction).

    Returns:
    - A JSON string containing the model response.
    """
    llm = ChatOpenAI(temperature=1, model="gpt-3.5-turbo")

    try:
        # Using Jinja2 to render the prompt from the template
        prompt = PromptManager.get_prompt(prompt_temp_name, **kwargs)
        # Invoke the LLM with the prompt
        response = llm.invoke(prompt)
        # Debug: Print the model response
        response_text = response.content

        # Parse the response assuming it's a JSON string
        response_data = json.loads(response_text)

        # Extract the necessary fields from the response
        feedback = response_data.get("feedback", {})

        return json.dumps(feedback, indent=2)  # Return the response as a JSON string, formatted nicely

    except Exception as e:
        # Handle any exceptions and return an error message in JSON format
        error_response = {
            "error": str(e)
        }
        return json.dumps(error_response)


if __name__ == "__main__":
    from pydantic import BaseModel
    from typing import List
    import pprint
    
    setup_environment()
  
    # Template name for generating explanation and suggestions
    prompt_temp_name = "third"  
    
    # Example input with a question, argument, and reasons for deduction
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
        """,
        "deductions": [
            "The argument lacks sufficient consideration of privacy concerns.",
            "The potential for bias in AI algorithms was not adequately addressed.",
            "There is no mention of the ethical implications regarding patient data security.",
            "The argument could be clearer in addressing the balance between AI benefits and human oversight."
        ]
    }

    # Call the function to generate the explanation and suggestions
    json_output = generate_explanation(ThirdPromptClass, prompt_temp_name, **kwargs_example)

    # Print the JSON output
    print(json_output)
