import os
import asyncio
import contextlib
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

TARGET_URL = os.getenv("SERVICE_A_URL", "http://business_service:8000/health")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async def ping_loop():
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    resp = await client.get(TARGET_URL, timeout=5)
                    print(f"[ping → {resp.status_code}]")
                except Exception as e:
                    print("Ping error:", e)
                await asyncio.sleep(10)

    app.state.ping_task = asyncio.create_task(ping_loop())

    yield

    app.state.ping_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await app.state.ping_task

app = FastAPI(lifespan=lifespan)

@app.get("/status")
def read_status():
    return {"message": "Service B running. Pinging Service A every 10s."}
