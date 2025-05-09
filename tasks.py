from celery_app import celery_app
from business_service.logic import perform_business_logic

@celery_app.task(name='itarch.process_data')
def process_data_async(data: dict) -> dict:
    """
    Wrapper to run business logic asynchronously.
    """
    return perform_business_logic(data)