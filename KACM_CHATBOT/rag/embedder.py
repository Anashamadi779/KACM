from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-m3",
    device="cpu",
    trust_remote_code=True
)

def get_embedding(text: str):
    """
    Convert text → 1024-dim vector
    Safe for Qdrant + Streamlit + Groq pipeline
    """
    if not text or not isinstance(text, str):
        return [0.0] * 1024

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()