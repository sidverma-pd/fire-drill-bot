import requests
import random
import datetime
import os

PAGERDUTY_API_KEY = os.environ['PD_API_KEY']
SERVICE_ID = os.environ['PD_SERVICE_ID']
ONCALL_USER_ID = os.environ['PD_USER_ID']

def lambda_handler(event, context):
    # Only trigger between 10am–4pm local
    now = datetime.datetime.now()
    if now.weekday() >= 5 or not (10 <= now.hour < 16):
        return { "status": "outside business hours" }

    # Random skip logic (40% chance to trigger)
    if random.random() > 0.4:
        return { "status": "skipped randomly" }

    incident_title = random.choice([
        "🔥 Fire Drill: Disk space at 95%",
        "🔥 Fire Drill: CPU spike on backend pod",
        "🔥 Fire Drill: High error rate on API gateway",
    ])

    payload = {
        "incident": {
            "type": "incident",
            "title": incident_title,
            "service": { "id": SERVICE_ID, "type": "service_reference" },
            "assignments": [{ "assignee": { "id": ONCALL_USER_ID, "type": "user_reference" } }],
            "urgency": "high"
        }
    }

    headers = {
        "Authorization": f"Token token={PAGERDUTY_API_KEY}",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Content-Type": "application/json"
    }

    r = requests.post("https://api.pagerduty.com/incidents", json=payload, headers=headers)

    return {
        "statusCode": r.status_code,
        "body": r.json()
    } 