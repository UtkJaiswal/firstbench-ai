import json  
import jinja2
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langsmith import traceable

# Load environment variables
load_dotenv()
OpenAI_key = os.getenv("OPENAI_API_KEY")

# Define template directory path
template_dir = "/home/kushagra/Downloads/Untitled/debate/prompts"

# Function to load and render the Jinja2 template
def load_template(template_name: str, template_dir: str, **kwargs) -> str:
    try:
        # Set up Jinja2 environment to load templates from the specified directory
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

        # Load the template by name
        template = env.get_template(template_name)
        print("template", template.inspect())
        # Render the template with provided arguments (kwargs)
        return template.render(**kwargs)

    except jinja2.TemplateNotFound:
        raise ValueError(f"Template '{template_name}' not found in directory '{template_dir}'.")
    except jinja2.TemplateError as e:
        raise ValueError(f"Error rendering template '{template_name}': {str(e)}")

# Test function that interacts with OpenAI and renders templates
@traceable
def test(temp_name: str, **kwargs) -> str:
    """
    Tests the OpenAI model with a given template and arguments, returning the response in JSON format.

    Parameters:
    - temp_name: The name of the template to be used for the prompt.
    - kwargs: Additional arguments for the prompt rendering.

    Returns:
    - A JSON string containing the model response.
    """
    llm = ChatOpenAI(temperature=1, 
                     model="gpt-3.5-turbo", 
                     openai_api_key=OpenAI_key)
    
    try:
        # Load and render the template
        print("kwargs", kwargs)
        prompt = load_template(temp_name, template_dir, **kwargs)

        # Invoke the language model with the rendered prompt
        response = llm.invoke(prompt)  # Use invoke instead of __call__

        # Extract the text response
        response_text = response.content

        # Return the response as JSON
        return json.dumps({"response": response_text})

    except Exception as e:
        # Handle any exceptions and return an error message in JSON format
        error_response = {
            "error": str(e)
        }
        return json.dumps(error_response)

if __name__ == "__main__":
    # Example usage
    # Define the sample template name
    template_name = "first.j2"  # Replace with your actual template file name

    # Example kwargs for the template
    kwargs_example = {
        "question": "What are the benefits of AI in healthcare?",
        "user_argument": "AI can improve diagnostic accuracy and patient care."
    }

    # Call the test function and print the result
    json_output = test(template_name, **kwargs_example)
    print(json_output)
