from xmlrpc import client

import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient


# ========== PAGE CONFIG (must be first Streamlit call) ==========
st.set_page_config(
    page_title="KAWKAB MARRAKECH AI Chatbot",
    page_icon="C:\\Users\\anash\\OneDrive\\Desktop\\KACM_CHATBOT\\Kawkab_Marrakech_(_KACM_)_Logo_png.png"
)

# ========== GROQ CLIENT ==========
groq_api_key = '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'

@st.cache_resource
def load_groq_client():
    return Groq(api_key=groq_api_key)

# ========== EMBEDDER ==========
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "BAAI/bge-m3",
        device="cpu",
        trust_remote_code=True
    )

def get_embedding(text: str):
    """Convert text → 1024-dim vector"""
    if not text or not isinstance(text, str):
        return [0.0] * 1024
    model = load_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

# ========== QDRANT CLIENT ==========
qdrant_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6NjE3MzQzM2YtMmE3OS00NjliLTk2NmQtNjM1YjM2ODQ0MTBhIn0.mC55kz2HDUkzJSiNde4lt2cOXqHlFKG0o7Rof54RqDI'
qdrant_url = 'https://6a773a3f-65fd-4f7d-9f91-90336b2f50b7.us-west-1-0.aws.cloud.qdrant.io'
COLLECTION_NAME = "botola_pro_rag"

@st.cache_resource
def load_qdrant_client():
    return QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

# ========== SEARCH FUNCTION ==========
def search(query: str, top_k: int = 3):
    """Semantic search in Qdrant using query_points (qdrant-client >= 1.7)"""
    if not query or not isinstance(query, str):
        return []

    try:
        query_vector = get_embedding(query)
        client = load_qdrant_client()

        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k
        ).points

        return results

    except Exception as e:
        st.error(f"Search error: {e}")
        return []

# ========== GENERATOR FUNCTION ==========
def generate_answer(context: str, question: str):
    client = Groq()
    completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
            {
                "role": "user",
                "content": "kawkab marrakech football club is a football club based in marrakech, morocco. the club was founded in 1947 and has a rich history in moroccan football. kawkab marrakech has won several domestic titles, including the botola pro (moroccan league) and the coupe du trone (moroccan cup). the club's colors are red and green, and they play their home matches at the stade de marrakech. kawkab marrakech has a passionate fan base and is known for its competitive spirit on the field. if you have any specific questions about kawkab marrakech, feel free to ask!"
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")


# ========== MAIN PIPELINE ==========
def ask_KAWKABI(question: str):
    # 1. Retrieve relevant docs
    results = search(question)

    if not results:
        return "No relevant information found in the database."

    # 2. Build context
    context = "\n\n".join([
        r.payload.get("text", "").strip()
        for r in results
        if r.payload and r.payload.get("text", "").strip()
    ])

    if not context.strip():
        return "No text content found in the retrieved documents."

    # 3. Generate answer
    return generate_answer(context, question)

# ========== STREAMLIT UI ==========
st.title("🇲🇦 KAWKAB MARRAKECH AI Chatbot")
st.markdown("Ask anything about **KAWKAB MARRAKECH FOOTBALL CLUB**")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Type your question here..."):
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_KAWKABI(question)
        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})