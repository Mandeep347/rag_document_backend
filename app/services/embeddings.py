import requests
from app.core.config import settings

def embed_text(text: str) -> list[float]:
    response = requests.post(
        "https://api.cohere.com/v1/embed",
        headers={"Authorization": f"Bearer {settings.cohere_api_key}"},
        json={"texts": [text], "model": "embed-english-light-v3.0", "input_type": "search_document"},
    )

    response.raise_for_status()
    return response.json()["embeddings"][0]