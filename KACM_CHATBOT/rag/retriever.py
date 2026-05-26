import qdrant_manager
import embedder

def search(query: str, top_k: int = 3):
    client = qdrant_manager.get_client()
    vector = embedder.get_embedding(query)
    
    results = client.search(
        collection_name=qdrant_manager.COLLECTION_NAME,
        query_vector=vector,
        limit=top_k
    )
    
    return results