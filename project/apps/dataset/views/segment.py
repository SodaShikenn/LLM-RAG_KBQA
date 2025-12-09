from flask import render_template, request, redirect, url_for, flash
from extensions.ext_database import db
from ..models import Dataset, Document, Segment
from .. import bp

@bp.route("/segment/<int:document_id>", endpoint="segment_list")
def segment_list(document_id):
    document = Document.query.filter_by(id=document_id).first()
    dataset = Dataset.query.filter_by(id=document.dataset_id).first()
    segments = Segment.query.filter_by(document_id=document_id).order_by(Segment.order.asc()).all()
    return render_template("dataset/segment_list.html", segments=segments, document=document, dataset=dataset)

@bp.route("/segment_create/<int:document_id>", methods=["GET", "POST"], endpoint="segment_create")
def create(document_id):
    pass

@bp.route("/segment_edit/<int:segment_id>", methods=["GET", "POST"], endpoint="segment_edit")
def edit(segment_id):
    pass

@bp.route("/segment_delete/<int:segment_id>", endpoint="segment_delete")
def delete(segment_id):
    pass