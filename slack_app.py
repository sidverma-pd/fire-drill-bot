import os
import random
from flask import Flask, request, make_response
from slack_sdk.signature import SignatureVerifier
from incident_titles import incident_titles
from pagerduty_client import trigger_incident
from incident_logic import poll_incident_updates
from slack_client import post_message, post_feedback_response

app = Flask(__name__)
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

@app.route('/slack/command', methods=['POST'])
def slack_command():
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid signature", 403)
    command = request.form.get('command')
    user_id = request.form.get('user_id')
    if command == '/trigger-drill':
        from datetime import datetime
        now = datetime.now()
        if now.weekday() >= 5 or not (9 <= now.hour < 17):
            return make_response("Fire drills can only be triggered during business hours (9am–5pm, Mon–Fri).", 200)
        incident_choice = random.choice(incident_titles)
        incident_title = incident_choice["title"]
        incident_urgency = incident_choice["urgency"]
        incident = trigger_incident(incident_title, incident_urgency)
        if incident:
            incident_id = incident['id']
            post_message(text=f"🚨 Fire drill triggered by <@{user_id}>: *{incident_title}*\nIncident ID: {incident_id}")
            import threading
            threading.Thread(target=poll_incident_updates, args=(incident_id, user_id), daemon=True).start()
            return make_response(f"Fire drill triggered! Incident ID: {incident_id}", 200)
        else:
            return make_response(f"Failed to trigger fire drill.", 200)
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
        post_feedback_response(user, action)
        return make_response("", 200)
    return make_response("No payload", 400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050) 