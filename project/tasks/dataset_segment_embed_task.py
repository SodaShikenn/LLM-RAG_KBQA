from celery import shared_task
import os
from apps.dataset.models import Document, Segment
from config import *
from extensions.ext_database import db
from helper import get_llm_embedding
from apps.dataset.milvus_models import DatasetMilvusModel


@shared_task(queue='dataset')
def task(document_id=None, segment_id=None):
    try:
        # Create index for entire document
        if document_id:
            document = Document.query.filter_by(id=document_id).first()
            segments = Segment.query.filter_by(document_id=document_id).all()

            # Delete Milvus data for this document_id
            delete_expr = f'document_id == {document_id}'
            DatasetMilvusModel.delete(delete_expr)

            # Prepare batch data for insertion
            batch_data = []
            for segment in segments:
                # Get text embedding
                response = get_llm_embedding(segment.content)
                text_vector = response.data[0].embedding
                batch_data.append({
                    'dataset_id': segment.dataset_id,
                    'document_id': segment.document_id,
                    'segment_id': segment.id,
                    'text_vector': text_vector
                })
                # Update segment status
                segment.status = 'completed'

            # Batch insert all segments at once to avoid timestamp lag
            if batch_data:
                DatasetMilvusModel.insert(batch_data)

            # Update document status
            document.status = 'completed'
            db.session.commit()
            print('exec dataset_segment_embed_task success.')

        # Insert or update segment
        if segment_id:
            segment = Segment.query.filter_by(id=segment_id).first()
            # Delete Milvus data for this segment_id
            delete_expr = f'segment_id == {segment_id}'
            DatasetMilvusModel.delete(delete_expr)
            # Get text embedding and store
            response = get_llm_embedding(segment.content)
            text_vector = response.data[0].embedding
            DatasetMilvusModel.insert([{
                'dataset_id': segment.dataset_id,
                'document_id': segment.document_id,
                'segment_id': segment.id,
                'text_vector': text_vector
            }])
            # Update segment status
            segment.status = 'completed'
            db.session.commit()
            print('exec dataset_segment_embed_task success.')
            
    except Exception as e:
        db.session.rollback()
        print(f'exec dataset_segment_embed_task error. {e}')