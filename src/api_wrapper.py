from flask import Flask, request, jsonify
from prompt_1 import argument_genre
from prompt_2 import test_evaluation
from prompt_3 import generate_explanation
from pydantic import BaseModel
from typing import List
import pprint
from utils.env import *
from utils.object import *
from utils.jinja import *
app = Flask(__name__)
setup_environment()

@app.route('/')
def a():
    p="this is a develoment server to acces the work go to these api 1 /api/argument_genre  2 /api/test_evaluation 3 /api/generate_explanation"
    return p
@app.route('/api/argument_genre', methods=['POST'])
def api_argument_genre():
    data = request.json
    prompt_temp_name = "first"
    kwargs = data.get('kwargs', {})
    response = argument_genre(FirstPromptClass, prompt_temp_name, **kwargs)
    
    return (response)

@app.route('/api/test_evaluation', methods=['POST'])
def api_test_evaluation():
    data = request.json
    prompt_temp_name = "second"
    kwargs = data.get('kwargs', {})
    response = test_evaluation(SecondPromptClass, prompt_temp_name, **kwargs)
    return (response)

@app.route('/api/generate_explanation', methods=['POST'])
def api_generate_explanation():
    data = request.json
    prompt_temp_name = "third"
    kwargs = data.get('kwargs', {})
    response = generate_explanation(ThirdPromptClass, prompt_temp_name, **kwargs)
    return (response)

if __name__ == '__main__':
    app.run(debug=True)