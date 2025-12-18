from flask import render_template, request, Response
from extensions.ext_database import db
from . import bp
from config import LLM_MODELS
from apps.dataset.models import Dataset

@bp.route('/', endpoint='index')
def index():
    dataset_objs = Dataset.query.order_by(Dataset.id.desc()).all()
    data = {
        'llm_models': list(LLM_MODELS.keys()),
        'datasets': [{'id': obj.id, 'name': obj.name} for obj in dataset_objs],
    }
    return render_template('chat/index.html', **data)



