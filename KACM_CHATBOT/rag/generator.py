from groq import Groq

groq_api_key = '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'
groq_client = Groq(api_key=groq_api_key)

def generate_answer(context: str, question: str):
    prompt = f"""
You are an expert on KAWKAB MARRAKECH FOOTBALL CLUB.

Answer ONLY using the context below.

If the answer is not in the context, say "I don't know based on available data."

Context:
{context}

Question:
{question}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content