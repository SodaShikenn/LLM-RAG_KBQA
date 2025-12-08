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
    return render_template("dataset/document_list.html", dataset=dataset)

@bp.route("/document_create/<int:dataset_id>", methods=["GET", "POST"], endpoint="document_create")
def create(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id).first()

    if request.method == "POST":
        # 处理文件上传
        file = request.files.get('file')
        if file:
            if not allowed_file(file.filename):
                flash("不允许的文件类型。只允许以下类型: " + ", ".join(ALLOWED_EXTENSIONS), 'error')
            elif file.content_length > MAX_CONTENT_LENGTH:
                flash("文件大小超过限制。最大允许大小为 16MB。", 'error')
            else:
                try:
                    # 提取文件扩展名
                    file_ext = os.path.splitext(file.filename)[1]
                    # 生成新的文件名
                    file_path = f"{uuid.uuid4()}{file_ext}"
                    # 保存文件
                    file.save(os.path.join(UPLOAD_FOLDER, file_path))

                    # 保存数据
                    new_document = Document(
                        dataset_id=dataset_id,
                        file_name=file.filename,
                        file_path=file_path,
                        status='init'
                    )
                    db.session.add(new_document)
                    db.session.commit()

                    # @todo 发起文件分割任务

                    flash("文件上传成功", "success")
                    return redirect(url_for("dataset.document_list", dataset_id=dataset_id))
                except Exception as e:
                    db.session.rollback()
                    flash(f"文件上传失败: {e}", "error")
    
    # Render the page
    return render_template("dataset/document_create.html", dataset=dataset)