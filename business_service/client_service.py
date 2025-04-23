from fastapi import FastAPI, Header, HTTPException
import requests
import os

client_app = FastAPI()
APP_TOKEN = os.getenv("APP_TOKEN")
db_url = "http://0.0.0.0:8001"
b_url = "http://0.0.0.0:8000"

@client_app.get("/")
def root():
    return {"message": "Client Service"}

@client_app.get("/health")
def health():
    return {"status": "Doing well"}

@client_app.get("/execute")
def execute(authorization: str = Header(None)):
    print(APP_TOKEN)
    if authorization != f"Bearer {APP_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    key, value = "message", "The world is going to end"
    response = requests.get(db_url+"/read", params={"key": key})
    data = response.json()
    print(data)
    processed_data = requests.post(b_url+"/process", json={"message": data["data"]})
    print(processed_data.json())
    print("_________")
    requests.post(db_url+"/write", json={"key": key, "value": processed_data.json()["processed"]})
    return {"message": "Data processed and saved"}
