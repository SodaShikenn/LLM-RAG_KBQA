import click
from pymilvus import connections
from apps.dataset.milvus_models import DatasetMilvusModel


@click.command("dataset_init_milvus")
def run():

    # Check connection status
    if connections.has_connection("default"):
        print("Successfully connected to Milvus")
    else:
        print("Failed to connect to Milvus")

    # Drop collection
    DatasetMilvusModel.drop_collection()

    # Initialize collection and create index
    DatasetMilvusModel.init_collection()
    DatasetMilvusModel.create_index()

    click.echo("[command] init_milvus success.")