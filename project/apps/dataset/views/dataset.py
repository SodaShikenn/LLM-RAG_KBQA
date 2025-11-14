from .. import bp
from flask import request, render_template, redirect, url_for, flash


@bp.route('/', endpoint='dataset_list')
def index():
    return render_template('dataset/dataset_list.html')

@bp.route('/dataset_create', endpoint='dataset_create')
def create():
    return render_template('dataset/dataset_create.html')







