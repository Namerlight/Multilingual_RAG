import os
import numpy as np
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client import models
from qdrant_client.models import Distance, VectorParams, PointStruct

from preprocess_data import process_data_file


def load_data(data_file_path: str, clean_output: bool = True) -> [str]:
    """
    Loads data by calling the preprocessing functions on the document.

    Args:
        data_file_path: path to the document file
        clean_output: whether or not to clean the output text

    Returns: a list of cleaned texts
    """

    processed_text = process_data_file(file_path=data_file_path, save_txt=False, clean_output=clean_output)

    return processed_text

def create_text_embedding(source_text: str) -> np.ndarray:
    """
    Generates the text embedding. One vector per line of text from the document.

    Args:
        source_text: list of texts as a string

    Returns: a 2D numpy array of text embeddings
    """

    text_to_embed = [f"query: {txt}" for txt in source_text]

    model = SentenceTransformer('intfloat/multilingual-e5-base')
    embeddings = model.encode(text_to_embed, normalize_embeddings=True, device='cuda:0')

    return embeddings


def store_vector(texts_to_store: list, embeddings_to_store: list) -> None:
    """
    Stores vectors stored in the qdrant vector DB.

    Args:
        texts_to_store: lines of text extracted from the document.
        embeddings_to_store: feature vectors for each text
    """

    client = QdrantClient(path=os.path.join("..", "database"))

    client.create_collection(
        "10MS_RAG",
        vectors_config=models.VectorParams(
            size=768, distance=models.Distance.COSINE)
    )

    print(len(embeddings_to_store), len(embeddings_to_store[0]))

    points = [
        PointStruct(id=idx, vector=embeddings_to_store[idx], payload={"text": texts_to_store[idx]})
        for idx in range(len(texts_to_store))
    ]

    client.upsert(
        collection_name="10MS_RAG",
        points=points
    )


if __name__ == '__main__':

    data_source = os.path.join("..", "data")
    data_files = os.listdir(data_source)

    text_data, embeddings_data = [], []

    for file in data_files:
        text_data += load_data(data_file_path=os.path.join(data_source, file))
        embeddings_data += create_text_embedding(source_text=text_data).tolist()

    store_vector(texts_to_store=text_data, embeddings_to_store=embeddings_data)


