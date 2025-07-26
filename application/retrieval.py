import os
import yaml
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models


class RAGSystem:

    def __init__(self) -> None:
        path_to_envs = os.path.join("..", "envs", "keys.yaml")

        with open(path_to_envs, "r") as f:
            config = yaml.safe_load(f)

        self.client = OpenAI(api_key=config["openai"]["api_key"])
        self.history = ""

    def generate_response(self, user_query: str, store_history: bool = False) -> str:
        """
        Takes the user's question and places it in a prompt. Calls the retrieval function to fetch information related
        to the question. Stores the chat history in a self.history variable.

        Args:
            user_query: The user's question.
            store_history: Whether to use the chat history for outputs, or just a single prompt.

        Returns: an output returned by the retrieval function.
        """

        prompt = f"""{user_query}

            Use the following information to help answer the question.

            {fetch_relevant_texts(user_query)}

            Answer in same language as the question. Keep it short - one or two words."""

        self.history += f"\n{prompt}"

        if store_history:
            input_to_model = f"{self.history}"
        else: input_to_model = prompt

        response = self.client.responses.create(
            model="gpt-4o",
            input=input_to_model
        )

        output = response.output_text

        self.history += f"\n{output}"

        return output



def fetch_relevant_texts(input_text: str) -> str:
    """
    Fetches text that's relevant to the user's input from the vector database

    Args:
        input_text: User's query text.

    Returns: a string containing a list of relevant texts from the database.
    """

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