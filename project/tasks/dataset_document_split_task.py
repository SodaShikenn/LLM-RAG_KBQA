import click
import os
import fitz  # PyMuPDF
import docx  # python-docx
import pandas as pd
from apps.dataset.models import Document, Segment
from config import *
from extensions.ext_database import db
from helper import segment_text
from celery import shared_task
from .dataset_segment_embed_task import task as dataset_segment_embed_task


@shared_task(queue='dataset')
def task(document_id):
    document = Document.query.filter_by(id=document_id).first()
    # Load and split files
    file_path = os.path.join(UPLOAD_FOLDER, document.file_path)
    segments = load_and_split(file_path)
    try:
        # Store segments
        for i, content in enumerate(segments):
            # Append document information for reference
            content = f'File "{document.file_name}", segment {i+1}, content:\n{content}'
            new_segment = Segment(
                dataset_id = document.dataset_id,
                document_id = document.id,
                order = i + 1,
                content = content,
                status = 'init'
            )
            db.session.add(new_segment)
        # Update document status
        document.status = 'indexing'
        
        # Trigger embedding task, delay 10 seconds to wait for transaction commit
        dataset_segment_embed_task.apply_async(
            kwargs = {'document_id': document_id},
            countdown = 10
        )

        db.session.commit()

        print('exec dataset_document_split_task success.')
    except Exception as e:
        db.session.rollback()
        print(f'exec dataset_document_split_task error. {e}')


def load_and_split(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_ext = file_extension[1:]
    # Process by suffix
    if file_ext == 'pdf':
        return process_pdf(file_path)
    if file_ext == 'txt':
        return process_txt(file_path)
    if file_ext == 'docx':
        return process_word(file_path)
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

def process_pdf(file_path):
    # Read PDF file content
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    # Segment text into chunks
    return segment_text(text, SEGMENT_LENGTH, OVERLAP)

def process_txt(file_path):
    with open(file_path, encoding='utf-8') as file:
        text = file.read()
    return segment_text(text, SEGMENT_LENGTH, OVERLAP)

def process_word(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return segment_text(text, SEGMENT_LENGTH, OVERLAP)