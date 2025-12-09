import os
from .. import bp
from flask import request, render_template, redirect, url_for, flash
from extensions.ext_database import db
from config import *
from ..models import Dataset, Document, Segment
from ..forms import DatasetForm
from sqlalchemy.sql import func

@bp.route('/', endpoint='dataset_list')
def list():
    datasets = (
        db.session.query(
            Dataset.id,
            Dataset.name,
            Dataset.desc,
            Dataset.created_at,
            func.count(Document.id).label("document_count"),
        )
        .outerjoin(Document, Dataset.id == Document.dataset_id)
        .group_by(Dataset.id)
        .order_by(Dataset.id.desc())
        .all()
    )
    return render_template('dataset/dataset_list.html', datasets=datasets)


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
        documents = Document.query.filter_by(dataset_id=dataset_id).all()
        # Delete local files
        for document in documents:
            file_full_path = os.path.join(UPLOAD_FOLDER, document.file_path)
            if os.path.exists(file_full_path):
                os.remove(file_full_path)

        Dataset.query.filter_by(id=dataset_id).delete()
        Document.query.filter_by(dataset_id=dataset_id).delete()
        Segment.query.filter_by(dataset_id=dataset_id).delete()
        # Commit transaction
        db.session.commit()

        flash("KB Deleted Successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Operation Failed: {e}", "error")

    return redirect(url_for("dataset.dataset_list"))
    