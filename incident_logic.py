import threading
import time
import datetime
from pagerduty_client import get_incident
from slack_client import post_message

def poll_incident_updates(incident_id, user_id):
    acked = False
    resolved = False
    score = 100
    while not resolved:
        incident = get_incident(incident_id)
        if not incident:
            time.sleep(10)
            continue
        status = incident['status']
        ack_time = incident.get('acknowledged_at')
        resolve_time = incident.get('resolved_at')
        if not acked and ack_time:
            acked = True
            post_message(text=f"✅ Fire drill incident *{incident_id}* acknowledged at {ack_time}.")
        if not resolved and resolve_time:
            resolved = True
            post_message(text=f"🎉 Fire drill incident *{incident_id}* resolved at {resolve_time}.")
            # Post a summary report
            summary_blocks = format_summary(incident, score)
            post_message(blocks=summary_blocks)
        if not resolved:
            time.sleep(15)

def format_summary(incident, score):
    assignments = incident.get('assignments', [])
    if assignments and 'assignee' in assignments[0]:
        on_call = assignments[0]['assignee'].get('summary', 'Unknown')
    else:
        on_call = 'Unknown'
    ack_time = incident.get('acknowledged_at')
    ack_by = 'N/A'
    if incident.get('acknowledgements'):
        ack_by = incident['acknowledgements'][0]['acknowledger'].get('summary', 'N/A')
    resolve_time = incident.get('resolved_at')
    resolve_by = on_call
    tta = None
    if ack_time and incident.get('created_at'):
        tta = int((datetime.datetime.strptime(ack_time, "%Y-%m-%dT%H:%M:%SZ") -
                   datetime.datetime.strptime(incident['created_at'], "%Y-%m-%dT%H:%M:%SZ")).total_seconds())
    ttr = None
    if resolve_time and incident.get('created_at'):
        ttr = int((datetime.datetime.strptime(resolve_time, "%Y-%m-%dT%H:%M:%SZ") -
                   datetime.datetime.strptime(incident['created_at'], "%Y-%m-%dT%H:%M:%SZ")).total_seconds())
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": "🚨 *Fire Drill Summary*"}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*On-Call:*\n{on_call}"},
            {"type": "mrkdwn", "text": f"*Incident ID:*\n{incident['id']}"},
            {"type": "mrkdwn", "text": f"*Created:*\n{incident.get('created_at', 'N/A')}"},
            {"type": "mrkdwn", "text": f"*Acknowledged:*\n{ack_time or 'Not acknowledged'} by {ack_by}"},
            {"type": "mrkdwn", "text": f"*Resolved:*\n{resolve_time or 'Not resolved'} by {resolve_by}"},
            {"type": "mrkdwn", "text": f"*TTA:*\n{tta if tta is not None else 'N/A'}s"},
            {"type": "mrkdwn", "text": f"*TTR:*\n{ttr if ttr is not None else 'N/A'}s"},
            {"type": "mrkdwn", "text": f"*Score:*\n{score}/100"}
        ]},
        {"type": "actions", "elements": [
            {"type": "button", "text": {"type": "plain_text", "text": "👍 This was helpful"}, "value": "helpful", "action_id": "feedback_helpful"},
            {"type": "button", "text": {"type": "plain_text", "text": "👎 Needs improvement"}, "value": "needs_improvement", "action_id": "feedback_needs_improvement"}
        ]}
    ]
    return blocks 