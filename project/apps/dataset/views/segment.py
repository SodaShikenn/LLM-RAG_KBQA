from flask import render_template, request, redirect, url_for, flash
from extensions.ext_database import db
from ..models import Dataset, Document, Segment
from ..forms import SegmentForm
from .. import bp

@bp.route("/segment/<int:document_id>", endpoint="segment_list")
def segment_list(document_id):
    document = Document.query.filter_by(id=document_id).first()
    dataset = Dataset.query.filter_by(id=document.dataset_id).first()
    segments = Segment.query.filter_by(document_id=document_id).order_by(Segment.order.asc()).all()
    return render_template("dataset/segment_list.html", segments=segments, document=document, dataset=dataset)


@bp.route("/segment_create/<int:document_id>", methods=["GET", "POST"], endpoint="segment_create")
def create(document_id):
    document = Document.query.filter_by(id=document_id).first()
    # Handle form data
    form = SegmentForm(request.form)
    if request.method == "POST" and form.validate():
        content = form.content.data
        order = form.order.data

        # If no order provided, auto-assign next available order for this document
        if not order:
            max_order = db.session.query(db.func.max(Segment.order)).filter_by(document_id=document_id).scalar()
            order = (max_order or 0) + 1

        new_segment = Segment(
            dataset_id = document.dataset_id,
            document_id = document_id,
            content = content,
            order = order,
            status = 'init',
        )
        db.session.add(new_segment)
        db.session.commit()

        flash("Segment inserted successfully!", "success")
        return redirect(url_for("dataset.segment_list", document_id=document.id))
    else:
        if form.errors:
            error_msg = ' '.join([error[0] for error in form.errors.values()])
            flash(error_msg, "error")
    # Render the page
    return render_template("dataset/segment_create.html", document=document, form=form)


@bp.route("/segment_edit/<int:segment_id>", methods=["GET", "POST"], endpoint="segment_edit")
def edit(segment_id):
    segment = Segment.query.filter_by(id=segment_id).first()
    document = Document.query.filter_by(id=segment.document_id).first()

    # Handle form data
    form = SegmentForm(request.form, obj=segment)
    if request.method == "POST" and form.validate():
        segment.content = form.content.data
        segment.order = form.order.data
        db.session.commit()

        flash("Segment updated successfully!", "success")
        return redirect(url_for("dataset.segment_list", document_id=document.id))
    else:
        if form.errors:
            error_msg = ' '.join([error[0] for error in form.errors.values()])
            flash(error_msg, "error")

    # Render the page
    return render_template("dataset/segment_edit.html", segment=segment, document=document, form=form)

@bp.route("/segment_delete/<int:segment_id>", endpoint="segment_delete")
def delete(segment_id):
    segment = Segment.query.filter_by(id=segment_id).first()
    document_id = segment.document_id
    deleted_order = segment.order

    try:
        # Delete the segment
        Segment.query.filter_by(id=segment_id).delete()

        # Reorder remaining segments for this document
        remaining_segments = Segment.query.filter_by(document_id=document_id).order_by(Segment.order.asc()).all()
        for i, seg in enumerate(remaining_segments, start=1):
            seg.order = i

        # Commit transaction
        db.session.commit()

        flash("Segment deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Operation failed: {e}", "error")

    return redirect(url_for("dataset.segment_list", document_id=document_id))