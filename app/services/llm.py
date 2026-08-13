from groq import Groq
from app.core.config import settings

client = Groq(
    api_key= settings.groq_api_key
)

def ask_with_context(question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n".join(context_chunks)

    system_prompt = (
        "You are a helpful assistent. Answer the user's question using ONLY "
        "the context provided below. If the answer isn't in the context, "
        "say you don't know — do not make up information.\n\n"
        f"Context:\n{context_text}"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )

    return response.choices[0].message.content


def ask_with_context_stream(question: str, context_chunks: list[str]):
    context_text = "\n\n".join(context_chunks)

    system_prompt = (
        "You are a helpful assistent. Answer the user's question using ONLY "
        "the context provided below. If the answer isn't in the context, "
        "say you don't know — do not make up information.\n\n"
        f"Context:\n{context_text}"
    )

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        stream = True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta