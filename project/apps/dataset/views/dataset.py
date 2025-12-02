from .. import bp
from flask import request, render_template, redirect, url_for, flash
from extensions.ext_database import db
from ..models import Dataset

@bp.route('/', endpoint='dataset_list')
def index():
    return render_template('dataset/dataset_list.html')

@bp.route("/dataset_create", methods=['GET', 'POST'], endpoint="dataset_create")
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')

        # Create Dataset instance and insert data
        new_dataset = Dataset(name=name, desc=desc)
        db.session.add(new_dataset)
        db.session.commit()

        flash("KB Creation Successful!", "success")
        return redirect(url_for("dataset.dataset_list"))

    return render_template('dataset/dataset_create.html')







