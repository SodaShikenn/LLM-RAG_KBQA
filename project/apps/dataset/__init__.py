from flask import Blueprint

bp = Blueprint('dataset', __name__, url_prefix='/dataset', template_folder='../templates/')

from .views import dataset
