import os, uuid
from flask import request, render_template, redirect, url_for, flash
from extensions.ext_database import db
from config import *
from .. import bp
from ..models import Dataset, Document

@bp.route("/document_list/<int:dataset_id>", endpoint="document_list")
def list(dataset_id):
    return f"document_list - dataset_id:{dataset_id}"