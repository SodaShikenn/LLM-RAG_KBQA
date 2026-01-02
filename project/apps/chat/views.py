from flask import render_template, request, Response
from extensions.ext_database import db
from . import bp
from config import LLM_MODELS
from apps.dataset.models import Dataset
import time
from helper import *

@bp.route('/', endpoint='index')
def index():
    dataset_objs = Dataset.query.order_by(Dataset.id.desc()).all()
    data = {
        'llm_models': list(LLM_MODELS.keys()),
        'datasets': [{'id': obj.id, 'name': obj.name} for obj in dataset_objs],
    }
    return render_template('chat/index.html', **data)

@bp.route('/test', methods=['POST'])
def test():
    output = 'This is a simulated text output from a large language model'
    def generate():
        full_text = ''
        # Output content word by word
        for chunk in output:
            time.sleep(1)
            content = chunk
            if content:
                full_text += content
                yield 'data: ' + json_response(200, 'ok', {
                    'content': content,
                    'text': full_text
                }) + '\n\n'
    return Response(generate(), content_type='text/plain')

@bp.route('/completions', methods=['POST'], endpoint='completions')
def completions():
    # Receive parameters
    data = request.get_json()
    messages = data['messages']
    params = data['params']
    # Request LLM
    completion = get_llm_chat(messages[:10], params['model_name'], True)
    # Define generator
    def generate():
        full_text = ''
        # Output content word by word
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                full_text += content
                yield 'data: ' + json_response(200, 'ok', {
                    'content': content,
                    'text': full_text
                }) + '\n\n'
    return Response(generate(), content_type='text/plain')

