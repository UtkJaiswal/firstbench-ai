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
def test_evaluation(pydentic_class, prompt_temp_name: str, **kwargs) -> str:
    """
    Tests the OpenAI model with a given template and arguments for scoring the argument,
    returning the response in JSON format.

    Parameters:
    - response_class: A Pydantic model specifying the response class.
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

        # Reformat the response to match the expected structure
        scores = response_data.get("scores", {})
        dynamic_metrics_score = scores.get("dynamic_metrics_score", {})
        print("dynamic_metrics_score", dynamic_metrics_score)
        static_metrics_score = scores.get("static_metrics_score", [])

        # Construct the final output
        final_output = {
            "scores": {
                "dynamic_metrics": [
                    {
                        "metric": dynamic_metric.get("metric_name"),
                        "score": dynamic_metric.get("score")
                    } for dynamic_metric in dynamic_metrics_score
                ],
                "static_metrics": [
                    {
                        "metric": static_metric.get("metric_name"),
                        "score": static_metric.get("score")
                    } for static_metric in static_metrics_score
                ]
            },
            "deductions": response_data.get("deductions", [])
        }

        return json.dumps(final_output, indent=2)  # Return the response as a JSON string, formatted nicely

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
  
    prompt_temp_name ="second"  # The template name for evaluation
    
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
        "dynamic_metrics": {
            "Accuracy of Facts", "Detail of Explanation", "Engagement with Counterarguments","Potential for Bias", "Ethical Considerations"
        },
        "static_metrics": {
            "Clarity & Structure", "Logical Coherence", "Use of Evidence", "Persuasiveness", "Engagement"
        }
        
    }

    # Call the test_evaluation function
    json_output = test_evaluation(SecondPromptClass, prompt_temp_name, **kwargs_example)
    # Print the JSON output
    print(json_output)
