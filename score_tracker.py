import requests
import os
import csv
from datetime import datetime

PAGERDUTY_API_KEY = os.environ['PD_API_KEY']
SERVICE_ID = os.environ['PD_SERVICE_ID']

INCIDENT_TAG = "🔥 Fire Drill"
CSV_FILE = "fire_drill_scores.csv"

headers = {
    "Authorization": f"Token token={PAGERDUTY_API_KEY}",
    "Accept": "application/vnd.pagerduty+json;version=2"
}

def fetch_fire_drill_incidents():
    url = f"https://api.pagerduty.com/incidents?service_ids[]={SERVICE_ID}&limit=100"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return [i for i in resp.json().get('incidents', []) if INCIDENT_TAG in i['title']]

def parse_time(timestr):
    return datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ")

def score_incident(incident):
    create_time = parse_time(incident['created_at'])
    ack_time = parse_time(incident['acknowledged_at']) if incident.get('acknowledged_at') else None
    resolve_time = parse_time(incident['resolved_at']) if incident.get('resolved_at') else None
    tta = (ack_time - create_time).seconds if ack_time else None
    ttr = (resolve_time - create_time).seconds if resolve_time else None
    score = 100
    if tta is not None:
        score -= tta * 0.5
    if ttr is not None:
        score -= ttr * 0.2
    return {
        'id': incident['id'],
        'user': incident['assignments'][0]['assignee']['summary'],
        'tta': tta,
        'ttr': ttr,
        'score': max(0, int(score))
    }

def main():
    incidents = fetch_fire_drill_incidents()
    with open(CSV_FILE, 'w', newline='') as csvfile:
        fieldnames = ['id', 'user', 'tta', 'ttr', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for incident in incidents:
            result = score_incident(incident)
            writer.writerow(result)
    print(f"Wrote {len(incidents)} fire drill scores to {CSV_FILE}")

if __name__ == "__main__":
    main() 