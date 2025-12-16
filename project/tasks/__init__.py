# Import all tasks to ensure they are registered with Celery
from tasks.demo_task import task as demo_task
from tasks.dataset_document_split_task import task as dataset_document_split_task
from tasks.dataset_segment_embed_task import task as dataset_segment_embed_task

__all__ = [
    'demo_task',
    'dataset_document_split_task',
    'dataset_segment_embed_task',
]
