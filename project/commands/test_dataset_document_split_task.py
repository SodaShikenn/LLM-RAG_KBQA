import click
import os
import fitz  # PyMuPDF
import docx  # python-docx
import pandas as pd
from apps.dataset.models import Document, Segment
from config import *
# from helper import segment_text
from extensions.ext_database import db

@click.command("test_dataset_document_split_task")
def run():
    document_id = 3
    document = Document.query.filter_by(id=document_id).first()
    # 加载并分割文件
    file_path = os.path.join(UPLOAD_FOLDER, document.file_path)
    segments = load_and_split(file_path)

def load_and_split(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_ext = file_extension[1:]
    # 按后缀分开处理
    # if file_ext == 'pdf':
    #     return process_pdf(file_path)
    # if file_ext == 'txt':
    #     return process_txt(file_path)
    # if file_ext == 'docx':
    #     return process_word(file_path)
    if file_ext == 'csv':
        return process_csv(file_path)
    if file_ext == 'xlsx':
        return process_excel(file_path)
    return []

def process_csv(file_path):
    df = pd.read_csv(file_path)
    data = []
    for _, row in df.iterrows():
        row_str = ', '.join([f"{col}: {row[col]}" for col in df.columns])
        data.append(row_str)
    return data

def process_excel(file_path):
    df = pd.read_excel(file_path)
    data = []
    for _, row in df.iterrows():
        row_str = ', '.join([f"{col}: {row[col]}" for col in df.columns])
        data.append(row_str)
    return data