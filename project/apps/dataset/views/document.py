import os, uuid
from flask import request, render_template, redirect, url_for, flash
from extensions.ext_database import db
from config import *
from .. import bp
from ..models import Dataset, Document
from helper import *

@bp.route("/document_list/<int:dataset_id>", endpoint="document_list")
def list(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id).first()
    documents = Document.query.filter_by(dataset_id=dataset_id).order_by(Document.created_at.desc()).all()
    return render_template("dataset/document_list.html", dataset=dataset, documents=documents)

@bp.route("/document_create/<int:dataset_id>", methods=["GET", "POST"], endpoint="document_create")
def create(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id).first()

    if request.method == "POST":
        # Handle file upload
        file = request.files.get('file')
        if file:
            if not allowed_file(file.filename):
                flash("File type not allowed. Only the following types are allowed: " + ", ".join(ALLOWED_EXTENSIONS), 'error')
            elif file.content_length > MAX_CONTENT_LENGTH:
                flash("File size exceeds limit. Maximum allowed size is 16MB.", 'error')
            else:
                try:
                    # Extract file extension
                    file_ext = os.path.splitext(file.filename)[1]
                    # Generate new file name
                    file_path = f"{uuid.uuid4()}{file_ext}"
                    # Save file
                    file.save(os.path.join(UPLOAD_FOLDER, file_path))

                    # Save data
                    new_document = Document(
                        dataset_id=dataset_id,
                        file_name=file.filename,
                        file_path=file_path,
                        status='init'
                    )
                    db.session.add(new_document)
                    db.session.commit()

                    # @todo Initiate file splitting task

                    flash("File uploaded successfully", "success")
                    return redirect(url_for("dataset.document_list", dataset_id=dataset_id))
                except Exception as e:
                    db.session.rollback()
                    flash(f"File upload failed: {e}", "error")
    
    # Render the page
    return render_template("dataset/document_create.html", dataset=dataset)