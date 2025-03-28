from fastapi import FastAPI
import time
from typing import Dict
from openai import OpenAI

business_app = FastAPI()

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
    api_key="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",
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