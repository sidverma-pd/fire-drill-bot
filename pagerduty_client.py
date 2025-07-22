import requests
import os

PAGERDUTY_API_KEY = os.environ['PD_API_KEY']
PD_SERVICE_ID = os.environ['PD_SERVICE_ID']
PD_USER_ID = os.environ['PD_USER_ID']

HEADERS = {
    "Authorization": f"Token token={PAGERDUTY_API_KEY}",
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Content-Type": "application/json"
}

def trigger_incident(title, urgency):
    payload = {
        "incident": {
            "type": "incident",
            "title": title,
            "service": { "id": PD_SERVICE_ID, "type": "service_reference" },
            "assignments": [{ "assignee": { "id": PD_USER_ID, "type": "user_reference" } }],
            "urgency": urgency
        }
    }
    r = requests.post("https://api.pagerduty.com/incidents", json=payload, headers=HEADERS)
    if r.status_code == 201:
        return r.json()['incident']
    else:
        print(f"PagerDuty API error: {r.status_code} {r.text}")
        return None

def get_incident(incident_id):
    url = f"https://api.pagerduty.com/incidents/{incident_id}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()['incident']
    else:
        print(f"PagerDuty API error: {r.status_code} {r.text}")
        return None 