from pymilvus import connections, Collection, utility
from pymilvus.client.types import LoadState

def init_app(app):
    try:
        connections.connect(
            alias="default",
            host=app.config['MILVUS_HOST'],
            port=app.config['MILVUS_PORT']
        )
    except Exception as e:
        print(f"An error occurred while connecting to Milvus: {e}")

class MilvusBaseModel:
    collection_name = None
    schema = None
    index_params = None
    index_field_name = None

    @classmethod
    def init_collection(cls):
        # Initialize collection
        if cls.collection_name is None or cls.schema is None:
            raise ValueError("collection_name and schema must be defined in the subclass")
        # Check if collection exists
        collections = utility.list_collections()
        if cls.collection_name not in collections:
            cls.collection = Collection(name=cls.collection_name, schema=cls.schema)
            print(f"Collection '{cls.collection_name}' created.")
        else:
            cls.collection = Collection(name=cls.collection_name)
            print(f"Collection '{cls.collection_name}' already exists.")

    @classmethod
    def load_collection(cls):
        collection = Collection(name=cls.collection_name)
        # Check collection load status
        if utility.load_state(cls.collection_name) == LoadState.NotLoad:
            collection.load()
        return collection

    @classmethod
    def drop_collection(cls):
        collections = utility.list_collections()
        if cls.collection_name in collections:
            utility.drop_collection(cls.collection_name)
            print(f"Collection '{cls.collection_name}' has been deleted.")
        else:
            print(f"Collection '{cls.collection_name}' does not exist.")

    @classmethod
    def create_index(cls):
        collection = Collection(name=cls.collection_name)
        if cls.index_field_name is None:
            return None
        if not collection.has_index(index_name=cls.index_field_name):
            if cls.index_params is None:
                raise ValueError("index_params must be defined in the subclass")
            print(cls.index_field_name, cls.index_params)
            collection.create_index(field_name=cls.index_field_name, index_params=cls.index_params)
            print(f"Index created for collection '{cls.collection_name}'.")

    @classmethod
    def get_entity_count(cls):
        collection = cls.load_collection()
        # Get entity count in collection
        entity_count = collection.num_entities
        return entity_count

    @classmethod
    def insert(cls, data):
        collection = cls.load_collection()
        collection.insert(data)
        # Note: Not flushing here to avoid blocking. Milvus will auto-flush periodically.
        # Data may not be immediately visible in searches until auto-flush completes.

    @classmethod
    def query(cls, expr, output_fields=None):
        collection = cls.load_collection()
        if not output_fields:
            # Dynamically get all fields
            schema = collection.schema
            output_fields = [field.name for field in schema.fields]
        # Query data
        results = collection.query(expr=expr, output_fields=output_fields)
        return results

    @classmethod
    def delete(cls, expr):
        collection = cls.load_collection()
        collection.delete(expr)

    @classmethod
    def search(cls, query_vectors, top_k, expr=None, output_fields=None):
        collection = cls.load_collection()
        # Search data
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        if not output_fields:
            # Dynamically get all fields
            schema = collection.schema
            output_fields = [field.name for field in schema.fields]
        # Use guarantee_timestamp=0 to use the latest data without timestamp checking
        results = collection.search(
            query_vectors,
            cls.index_field_name,
            search_params,
            top_k,
            expr=expr,
            output_fields=output_fields,
            guarantee_timestamp=0  # Use the most up-to-date data
        )
        return results
