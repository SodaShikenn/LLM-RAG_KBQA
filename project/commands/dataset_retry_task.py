import click
from apps.dataset.models import Document, Segment
from tasks.dataset_document_split_task import task as dataset_document_split_task
from tasks.dataset_segment_embed_task import task as dataset_segment_embed_task
# from ..milvus_models import DatasetMilvusModel

@click.command("dataset_retry_task")
def run():
    # Retry document splitting
    documents = Document.query.filter_by(status='init').all()
    for document in documents:
        dataset_document_split_task.delay(document.id)

    # Retry document indexing
    documents = Document.query.filter_by(status='indexing').all()
    for document in documents:
        dataset_segment_embed_task.delay(document.id)

    # Retry segment indexing
    segments = Segment.query.filter_by(status='init').all()
    for segment in segments:
        dataset_segment_embed_task.delay(None, segment.id)

    click.echo("[command] dataset_retry_task success.")

# from ..milvus_models import DatasetMilvusModel

# # apps/dataset/views/dataset.py
# # 删除 milvus 数据
# delete_expr = f'dataset_id == {dataset_id}'
# DatasetMilvusModel.delete(delete_expr)

# # apps/dataset/views/document.py
# # 删除 milvus 数据
# delete_expr = f'document_id == {document_id}'
# DatasetMilvusModel.delete(delete_expr)

# # apps/dataset/views/segment.py
# # 删除 milvus 数据
# delete_expr = f'segment_id == {segment_id}'
# DatasetMilvusModel.delete(delete_expr)