from retriever import search
from generator import generate_answer

def ask_botola(question: str):
    # 1. Retrieve relevant docs
    results = search(question)
    
    if not results:
        return "No relevant information found."
    
    # 2. Build context
    context = "\n".join([
        r.payload.get("text", "") for r in results if r.payload and "text" in r.payload
    ])
    
    if not context.strip():
        return "No text content found."
    
    # 3. Generate answer
    answer = generate_answer(context, question)
    
    return answer