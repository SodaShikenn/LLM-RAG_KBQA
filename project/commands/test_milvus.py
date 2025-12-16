import click
from random import random
from pymilvus import connections
from apps.dataset.milvus_models import DatasetMilvusModel

@click.command("test_milvus")
def run():
    # Check Connection Status
    if connections.has_connection("default"):
        print("Successfully connected to Milvus")
    else:
        print("Failed to connect to Milvus")