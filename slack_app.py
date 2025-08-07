import os
import random
from flask import Flask, request, make_response
from slack_sdk.signature import SignatureVerifier
from incident_titles import incident_titles
from fire_drill_templates import get_template, get_all_templates, list_template_names
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
    command = request.form.get('command', '')
    user_id = request.form.get('user_id')
    text = request.form.get('text', '').strip()

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

    elif command == '/trigger-template':
        if not text:
            templates = list_template_names()
            template_list = "\n".join([f"• `{template}`" for template in templates])
            return make_response(f"Available templates:\n{template_list}\n\nUsage: `/trigger-template <template_name>`", 200)

        template_name = text.lower().replace(' ', '_')
        template = get_template(template_name)

        if not template:
            return make_response(f"Template '{text}' not found. Use `/trigger-template` to see available templates.", 200)

        incident_title = template["title"]
        incident_urgency = template["urgency"]
        incident = trigger_incident(incident_title, incident_urgency)

        if incident:
            incident_id = incident['id']
            description = template.get("description", "")
            difficulty = template.get("difficulty", "medium")
            category = template.get("category", "general")

            message = f"🚨 Template fire drill triggered by <@{user_id}>:\n"
            message += f"*{incident_title}*\n"
            message += f"Category: {category.title()}\n"
            message += f"Difficulty: {difficulty.title()}\n"
            if description:
                message += f"Description: {description}\n"
            message += f"Incident ID: {incident_id}"

            post_message(text=message)
            import threading
            threading.Thread(target=poll_incident_updates, args=(incident_id, user_id), daemon=True).start()
            return make_response(f"Template fire drill triggered! Incident ID: {incident_id}", 200)
        else:
            return make_response(f"Failed to trigger template fire drill.", 200)

    elif command == '/list-templates':
        templates = get_all_templates()
        template_list = []

        for name, template in templates.items():
            category = template.get('category', 'general')
            difficulty = template.get('difficulty', 'medium')
            urgency = template.get('urgency', 'high')
            template_list.append(f"• `{name}` ({category}, {difficulty}, {urgency})")

        template_text = "\n".join(template_list)
        return make_response(f"Available fire drill templates:\n{template_text}\n\nUse `/trigger-template <template_name>` to run a specific template.", 200)

    else:
        return make_response("Unknown command. Available commands: `/trigger-drill`, `/trigger-template`, `/list-templates`", 200)

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