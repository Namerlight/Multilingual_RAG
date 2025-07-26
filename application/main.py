from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import yaml
import os

from retrieval import fetch_relevant_texts

path_to_envs = os.path.join("..", "envs", "keys.yaml")

with open(path_to_envs, "r") as f:
    config = yaml.safe_load(f)
openai_api_key = config["openai"]["api_key"]

client = OpenAI(api_key=config["openai"]["api_key"])

app = FastAPI()

# Input model for POST request
class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "10MS_RAG"}

@app.post("/rag_chat")
def process_text(data: TextInput):

    prompt = f"""{data.text}

    Use the following information to help answer the question.

    {fetch_relevant_texts(data.text)}

    Answer in one line in the same language as the question."""

    response = client.responses.create(
        model="gpt-4o",
        input=f"User input: {data.text}"
    )

    output = response.output_text
    return {"processed_text": output}

