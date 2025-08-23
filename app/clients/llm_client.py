import os
from groq import Groq

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment")
        self.client = Groq(api_key=api_key)

    def generate_answer(self, question: str, context: str) -> str:
        prompt = (
            "You are a helpful assistant. Use the context below to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
        resp = self.client.chat.completions.create(
            model="llama3-8b-8192",  # Groq’s free model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content
