import os

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models


def fetch_relevant_texts(input_text: str):

    client = QdrantClient(path=os.path.join("..", "knowledge_base", "database"))

    text_to_embed = input_text

    model = SentenceTransformer('intfloat/multilingual-e5-base')
    embeddings = model.encode(text_to_embed, normalize_embeddings=True, device='cuda:0')

    query_vector = embeddings

    search_result = client.query_points(
        collection_name="10MS_RAG",
        query=query_vector,
        with_payload=True,
        limit=5
    )

    retrieved_texts = ""
    for point in search_result:
        _, scores = point
        for score in scores:
            print(score.payload)
            retrieved_texts += score.payload.get("text") + "\n"

    return retrieved_texts.strip()