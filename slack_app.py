import os
from flask import Flask, request, make_response, jsonify
from slack_sdk.web import WebClient
from slack_sdk.signature import SignatureVerifier
import requests
import random
import datetime
import threading
import time

app = Flask(__name__)

SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#oncall-fire-drills')

PD_API_KEY = os.environ['PD_API_KEY']
PD_SERVICE_ID = os.environ['PD_SERVICE_ID']
PD_USER_ID = os.environ['PD_USER_ID']

client = WebClient(token=SLACK_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

def poll_incident_updates(incident_id, user_id):
    """Poll PagerDuty for incident status and post updates to Slack."""
    url = f"https://api.pagerduty.com/incidents/{incident_id}"
    headers = {
        "Authorization": f"Token token={PD_API_KEY}",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    acked = False
    resolved = False
    while not resolved:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            time.sleep(10)
            continue
        incident = r.json()['incident']
        status = incident['status']
        ack_time = incident.get('acknowledged_at')
        resolve_time = incident.get('resolved_at')
        if not acked and ack_time:
            acked = True
            client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=f"✅ Fire drill incident *{incident_id}* acknowledged at {ack_time}."
            )
        if not resolved and resolve_time:
            resolved = True
            client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=f"🎉 Fire drill incident *{incident_id}* resolved at {resolve_time}."
            )
            # Post a summary report with advanced details and feedback buttons
            create_time = incident['created_at']
            tta = None
            ttr = None
            if ack_time:
                tta = int((datetime.datetime.strptime(ack_time, "%Y-%m-%dT%H:%M:%SZ") - datetime.datetime.strptime(create_time, "%Y-%m-%dT%H:%M:%SZ")).total_seconds())
            if resolve_time:
                ttr = int((datetime.datetime.strptime(resolve_time, "%Y-%m-%dT%H:%M:%SZ") - datetime.datetime.strptime(create_time, "%Y-%m-%dT%H:%M:%SZ")).total_seconds())
            score = 100
            if tta is not None:
                score -= tta * 0.5
            if ttr is not None:
                score -= ttr * 0.2
            score = max(0, int(score))
            user = incident['assignments'][0]['assignee']['summary']
            ack_by = incident['acknowledgements'][0]['acknowledger']['summary'] if incident.get('acknowledgements') else 'N/A'
            resolve_by = user  # PagerDuty API v2 does not always provide resolver, fallback to assignee
            blocks = [
                {"type": "section", "text": {"type": "mrkdwn", "text": "🚨 *Fire Drill Summary*"}},
                {"type": "section", "fields": [
                    {"type": "mrkdwn", "text": f"*On-Call:*\n{user}"},
                    {"type": "mrkdwn", "text": f"*Incident ID:*\n{incident_id}"},
                    {"type": "mrkdwn", "text": f"*Created:*\n{create_time}"},
                    {"type": "mrkdwn", "text": f"*Acknowledged:*\n{ack_time or 'N/A'} by {ack_by}"},
                    {"type": "mrkdwn", "text": f"*Resolved:*\n{resolve_time or 'N/A'} by {resolve_by}"},
                    {"type": "mrkdwn", "text": f"*TTA:*\n{tta if tta is not None else 'N/A'}s"},
                    {"type": "mrkdwn", "text": f"*TTR:*\n{ttr if ttr is not None else 'N/A'}s"},
                    {"type": "mrkdwn", "text": f"*Score:*\n{score}/100"}
                ]},
                {"type": "actions", "elements": [
                    {"type": "button", "text": {"type": "plain_text", "text": "👍 This was helpful"}, "value": "helpful", "action_id": "feedback_helpful"},
                    {"type": "button", "text": {"type": "plain_text", "text": "👎 Needs improvement"}, "value": "needs_improvement", "action_id": "feedback_needs_improvement"}
                ]}
            ]
            client.chat_postMessage(
                channel=SLACK_CHANNEL,
                blocks=blocks,
                text="Fire Drill Summary"
            )
        if not resolved:
            time.sleep(15)

@app.route('/slack/command', methods=['POST'])
def slack_command():
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid signature", 403)
    command = request.form.get('command')
    user_id = request.form.get('user_id')
    if command == '/trigger-drill':
        now = datetime.datetime.now()
        if now.weekday() >= 5 or not (9 <= now.hour < 17):
            return make_response("Fire drills can only be triggered during business hours (9am–5pm, Mon–Fri).", 200)
        incident_title = random.choice([
            "🔥 Fire Drill: Disk space at 95%",
            "🔥 Fire Drill: CPU spike on backend pod",
            "🔥 Fire Drill: High error rate on API gateway",
        ])
        payload = {
            "incident": {
                "type": "incident",
                "title": incident_title,
                "service": { "id": PD_SERVICE_ID, "type": "service_reference" },
                "assignments": [{ "assignee": { "id": PD_USER_ID, "type": "user_reference" } }],
                "urgency": "high"
            }
        }
        headers = {
            "Authorization": f"Token token={PD_API_KEY}",
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Content-Type": "application/json"
        }
        r = requests.post("https://api.pagerduty.com/incidents", json=payload, headers=headers)
        if r.status_code == 201:
            incident = r.json()['incident']
            incident_id = incident['id']
            client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=f"🚨 Fire drill triggered by <@{user_id}>: *{incident_title}*\nIncident ID: {incident_id}"
            )
            threading.Thread(target=poll_incident_updates, args=(incident_id, user_id), daemon=True).start()
            return make_response(f"Fire drill triggered! Incident ID: {incident_id}", 200)
        else:
            return make_response(f"Failed to trigger fire drill: {r.text}", 200)
    return make_response("Unknown command", 200)

@app.route('/slack/interactivity', methods=['POST'])
def slack_interactivity():
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid signature", 403)
    payload = request.form.get('payload')
    if payload:
        import json
        data = json.loads(payload)
        user = data['user']['id']
        action = data['actions'][0]['value']
        response_text = f"Thank you <@{user}> for your feedback: *{action}*."
        client.chat_postMessage(channel=SLACK_CHANNEL, text=response_text)
        return make_response("", 200)
    return make_response("No payload", 400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 