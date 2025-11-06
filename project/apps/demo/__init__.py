from flask import Blueprint

bp = Blueprint('demo', __name__, url_prefix='/demo', template_folder='../templates/')

from . import views
