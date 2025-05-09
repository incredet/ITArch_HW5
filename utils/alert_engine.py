import os
import datetime
import logging
import re

ALERT_DIR = 'error_reports'
os.makedirs(ALERT_DIR, exist_ok=True)


def generate_alert(alert_type: str, description: str):
    """
    Write a mini-report file in error_reports/ with timestamp, type, and description.
    Also logs a warning via the standard logger.
    """
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{ALERT_DIR}/alert_{alert_type}_{timestamp}.txt"
    content = (
        f"Time: {datetime.datetime.utcnow().isoformat()} UTC\n"
        f"Type: {alert_type}\n"
        f"Description: {description}\n"
    )
    with open(filename, 'w') as f:
        f.write(content)

    logging.getLogger(__name__).warning(f"Alert: {alert_type} - {description}")


def detect_invalid_input(data: dict) -> bool:
    required = ['user_id', 'action']
    return any(field not in data for field in required)


def detect_personal_data(data: dict) -> bool:
    text = str(data)
    ssn_pattern = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    if ssn_pattern.search(text):
        return True
    if 'email' in data:
        return True
    return False


def detect_fraud(data: dict) -> bool:
    amount = data.get('amount', 0)
    return isinstance(amount, (int, float)) and amount > 10000
