from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import yaml
import os

from retrieval import fetch_relevant_texts, RAGSystem

RAGQA = RAGSystem()
app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    print("Executing root request.")
    return {"message": "Multilingual RAG Application for 10MS Technical Assessment."}

@app.post("/rag_chat")
def process_text(data: TextInput):

    output = RAGQA.generate_response(user_query=data.text)

    return {"Answer": output}

