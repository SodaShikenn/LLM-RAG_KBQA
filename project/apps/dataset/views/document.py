import os, uuid
from flask import request, render_template, redirect, url_for, flash
from extensions.ext_database import db
from config import *
from .. import bp
from ..models import Dataset, Document

@bp.route("/document_list/<int:dataset_id>", endpoint="document_list")
def list(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id).first()
    return render_template("dataset/document_list.html", dataset=dataset)

@bp.route("/document_create/<int:dataset_id>", methods=["GET", "POST"], endpoint="document_create")
def create(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id).first()
    # Render the page
    return render_template("dataset/document_create.html", dataset=dataset)