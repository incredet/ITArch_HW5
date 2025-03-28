from fastapi import FastAPI
import time
from typing import Dict
from openai import OpenAI
import os

business_app = FastAPI()
openai_key = os.getenv("OPENAI_KEY")

@business_app.get("/")
def root():
    return {"message": "Business Logic Service"}

@business_app.get("/health")
def health():
    return {"status": "Doing well"}

@business_app.post("/process")
def process_data(payload: Dict):

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openai_key,
    )

    completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {
        "role": "user",
        "content": payload["message"]
        }
    ]
    )
    print(completion.choices[0].message.content)
    return {"original": payload, "processed": completion.choices[0].message.content}