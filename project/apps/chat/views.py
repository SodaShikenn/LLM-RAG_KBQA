from flask import render_template, request, Response
from extensions.ext_database import db
from . import bp
from config import LLM_MODELS
from apps.dataset.models import Dataset
import time
from helper import *
from .services import retrieve_related_texts
from .models import Conversation


@bp.route('/', endpoint='index')
def index():
    dataset_objs = Dataset.query.order_by(Dataset.id.desc()).all()
    conversation_objs = Conversation.query.with_entities(
        Conversation.id, Conversation.uid, Conversation.name
    ).order_by(Conversation.id.desc()).all()
    data = {
        'llm_models': list(LLM_MODELS.keys()),
        'datasets': [{'id': obj.id, 'name': obj.name} for obj in dataset_objs],
        'conversations': [{'uid': obj.uid, 'name': obj.name} for obj in conversation_objs],
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
    # If knowledge base is selected, append retrieved text
    if params['dataset_ids']:
        # Retrieve similar texts and add to messages
        messages = retrieve_related_texts(messages, params)

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


@bp.route('/conversation_create', methods=['POST'], endpoint='conversation_create')
def conversation_create():
    try:
        data = request.get_json()
        new_conversation = Conversation(
            uid = data['uid'],
            name = data['name'],
            messages = []
        )
        db.session.add(new_conversation)
        db.session.commit()
        return json_response(200, 'ok')
    except Exception as e:
        return json_response(500, f'error: {e}')


@bp.route('/conversation_delete', methods=['POST'], endpoint='conversation_delete')
def conversation_delete():
    try:
        data = request.get_json()
        conversation = Conversation.query.filter_by(
            uid = data['uid'],
        ).first()
        db.session.delete(conversation)
        db.session.commit()
        return json_response(200, 'ok')
    except Exception as e:
        return json_response(500, f'error: {e}')
    

@bp.route('/conversation_edit', methods=['POST'], endpoint='conversation_edit')
def conversation_edit():
    try:
        data = request.get_json()
        conversation = Conversation.query.filter_by(
            uid = data['uid'],
        ).first()
        conversation.name = data['name']
        db.session.commit()
        return json_response(200, 'ok')
    except Exception as e:
        return json_response(500, f'error: {e}')