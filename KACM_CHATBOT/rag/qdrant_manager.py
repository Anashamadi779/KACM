from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

qdrant_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6NjE3MzQzM2YtMmE3OS00NjliLTk2NmQtNjM1YjM2ODQ0MTBhIn0.mC55kz2HDUkzJSiNde4lt2cOXqHlFKG0o7Rof54RqDI'
qdrant_url = 'https://6a773a3f-65fd-4f7d-9f91-90336b2f50b7.us-west-1-0.aws.cloud.qdrant.io'

_qdrant_client = None

def get_client():
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key
        )
    return _qdrant_client

COLLECTION_NAME = "botola_pro_rag"

def create_collection():
    client = get_client()
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )
    print("Collection created successfully")