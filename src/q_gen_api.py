from flask import Flask, request, jsonify
from q_gen import generate_complex_question
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
    p="this is a develoment server to acces the work go to these api  /api/q_gen"
    return p
@app.route('/api/q_gen', methods=['POST'])
def api_argument_genre():
    data = request.json
    prompt_temp_name = "q_gen"
    kwargs = data.get('kwargs', {})
    response = generate_complex_question(FirstPromptClass, prompt_temp_name, **kwargs)
    
    return (response)


if __name__ == '__main__':
    app.run(debug=True)