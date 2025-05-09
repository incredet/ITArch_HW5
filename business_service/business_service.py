import os
import logging
from fastapi import FastAPI, HTTPException, Request
from json import JSONDecodeError
from utils.logging_config import setup_logging
from utils.alert_engine import (
    generate_alert, detect_invalid_input, detect_personal_data, detect_fraud
)
from tasks import process_data_async
from ..celery_app import celery_app

debug_log = os.getenv('DEBUG_LOG', 'false').lower() == 'true'
logger = setup_logging(log_file='logs/business_service.log')

app = FastAPI(title="Business Service")

@app.post("/process")
async def process(request: Request):
    # 1) catch totally invalid JSON
    try:
        data = await request.json()
    except JSONDecodeError:
        generate_alert(
            alert_type="invalid_json",
            description="Could not parse JSON body"
        )
        raise HTTPException(status_code=400, detail="Malformed JSON")

    required = {"user_id", "action", "amount"}
    missing = required - data.keys()
    if missing:
        generate_alert(
            alert_type="invalid_input",
            description=f"Missing fields: {', '.join(missing)}"
        )
        raise HTTPException(status_code=400, detail=f"Missing fields: {missing}")

    if detect_fraud(data):
        generate_alert(
            alert_type="fraud_attempt",
            description=f"High transaction amount: {data['amount']}"
        )
    if detect_personal_data(data):
        generate_alert(
            alert_type="personal_data",
            description="Payload contains personal identifiable information"
        )

    logger.info(f"Enqueuing async task for data: {data}")
    task = process_data_async.delay(data)
    return {"status": "queued", "task_id": task.id}

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    async_result = celery_app.AsyncResult(task_id)
    response = {"state": async_result.state}
    if async_result.successful():
        response["result"] = async_result.result
    elif async_result.failed():
        response["error"] = str(async_result.result)
    return response


def perform_business_logic(data: dict) -> dict:
    return data

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "business_service.business_service:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )