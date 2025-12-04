from .. import bp
from flask import request, render_template, redirect, url_for, flash
from extensions.ext_database import db
from ..models import Dataset
from ..forms import DatasetForm


@bp.route('/', endpoint='dataset_list')
def index():
    datasets = Dataset.query.order_by(Dataset.id.desc()).all()
    return render_template('dataset/dataset_list.html', datasets=datasets)
    return render_template('dataset/dataset_list.html')


@bp.route("/dataset_create", methods=["GET", "POST"], endpoint="dataset_create")
def create():
    form = DatasetForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        desc = form.desc.data

        # Create Dataset instance and insert data
        new_dataset = Dataset(name=name, desc=desc)
        db.session.add(new_dataset)
        db.session.commit()

        flash("KB Creation Successful!", "success")
        return redirect(url_for("dataset.dataset_list"))

    else:
        if form.errors:
            error_msg = ' '.join([error[0] for error in form.errors.values()])
            flash(error_msg, "error")
            
    # Render the page
    return render_template("dataset/dataset_create.html", form=form)

@bp.route("/dataset_edit/<int:dataset_id>", methods=["GET", "POST"], endpoint="dataset_edit")
def edit(dataset_id):
    form = DatasetForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        desc = form.desc.data

        dataset = Dataset.query.filter_by(id=dataset_id).first()
        dataset.name = name
        dataset.desc = desc
        db.session.commit()

        flash("KB Edited  Successfully!", "success")
        return redirect(url_for("dataset.dataset_list"))
    else:
        if form.errors:
            error_msg = ' '.join([error[0] for error in form.errors.values()])
            flash(error_msg, "error")
    # Query a single dataset entry
    dataset = Dataset.query.filter_by(id=dataset_id).first()
    return render_template("dataset/dataset_edit.html", dataset=dataset, form=form)

@bp.route("/dataset_delete/<int:dataset_id>", endpoint="dataset_delete")
def delete(dataset_id):
    try:
        Dataset.query.filter_by(id=dataset_id).delete()
        # Commit stuff
        db.session.commit()

        # @todo Delete all child data

        flash("KB Deleted Successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Operation Failed: {e}", "error")

    return redirect(url_for("dataset.dataset_list"))
    