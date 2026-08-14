import requests
from app.core.config import settings

COHERE_EMBED_URL = "https://api.cohere.com/v1/embed"

def embed_text(texts: list[str]) -> list[list[float]]:
    all_vectors = []
    batch_size = 90 #safety margin under cohere cap

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = requests.post(
            COHERE_EMBED_URL,
            headers={"Authorization": f"Bearer {settings.cohere_api_key}"},
            json={
                "texts": batch, 
                "model": "embed-english-light-v3.0", 
                "input_type": "search_document"
            },
        )
        response.raise_for_status()
        all_vectors.extend(response.json()["embeddings"])

    return all_vectors