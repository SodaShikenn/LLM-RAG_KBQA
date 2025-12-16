import click
from random import random
from pymilvus import connections
from apps.dataset.milvus_models import DatasetMilvusModel

@click.command("test_milvus")
def run():
    # Check connection status
    if connections.has_connection("default"):
        print("Successfully connected to Milvus")
    else:
        print("Failed to connect to Milvus")

    # # Initialize the collection and create an index
    # DatasetMilvusModel.init_collection()
    # DatasetMilvusModel.create_index()

    # # Insert data
    # data = [
    #     {"dataset_id": 1, "document_id": 1, "segment_id": 1, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 1, "document_id": 1, "segment_id": 2, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 2, "document_id": 2, "segment_id": 1, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 2, "document_id": 2, "segment_id": 2, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 2, "document_id": 2, "segment_id": 3, "text_vector": [random() for i in range(1536)]},
    # ]
    # DatasetMilvusModel.insert(data)

    # # Query data
    # records = DatasetMilvusModel.query('dataset_id==2')
    # print(records)
    # print(len(records))

    # # View data amount
    # print(DatasetMilvusModel.get_entity_count())

    # # Delete data
    # delete_expr = 'dataset_id==2'
    # DatasetMilvusModel.delete(delete_expr)

    # # Delete collection
    # DatasetMilvusModel.drop_collection()

    # Vector search
    query_vector = [random() for i in range(1536)]
    records = DatasetMilvusModel.search([query_vector], 3)
    for record in records[0]:
        print(record)