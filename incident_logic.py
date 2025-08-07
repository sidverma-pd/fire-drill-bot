import threading
import time
import datetime
from pagerduty_client import get_incident
from slack_client import post_message
from fire_drill_templates import get_all_templates

def poll_incident_updates(incident_id, user_id):
    """Poll PagerDuty for incident updates and post to Slack."""
    start_time = time.time()
    acknowledged_time = None
    resolved_time = None
    acknowledged_by = None
    resolved_by = None
    
    # Check if this incident was created from a template
    template_used = None
    templates = get_all_templates()
    
    while True:
        incident = get_incident(incident_id)
        if not incident:
            time.sleep(30)
            continue
        
        # Try to match incident title with a template
        if template_used is None:
            incident_title = incident.get('title', '')
            for template_name, template in templates.items():
                if template['title'] == incident_title:
                    template_used = template
                    break
        
        status = incident.get('status', '')
        
        if status == 'acknowledged' and acknowledged_time is None:
            acknowledged_time = time.time()
            acknowledged_by = get_assignee_name(incident)
            tta = int(acknowledged_time - start_time)
            post_message(text=f"✅ Incident acknowledged by {acknowledged_by} in {tta} seconds")
        
        elif status == 'resolved' and resolved_time is None:
            resolved_time = time.time()
            resolved_by = get_assignee_name(incident)
            ttr = int(resolved_time - start_time)
            post_message(text=f"🎉 Incident resolved by {resolved_by} in {ttr} seconds")
            
            # Calculate score and post summary
            score = calculate_score(start_time, acknowledged_time, resolved_time, template_used)
            summary_blocks = format_summary(incident, score, template_used)
            post_message(blocks=summary_blocks)
            break
        
        elif status == 'triggered':
            # Still waiting for acknowledgment
            pass
        
        time.sleep(30)

def get_assignee_name(incident):
    """Extract assignee name from incident data."""
    assignments = incident.get('assignments', [])
    if assignments and 'assignee' in assignments[0]:
        return assignments[0]['assignee'].get('summary', 'Unknown')
    return 'Unknown'

def calculate_score(start_time, acknowledged_time, resolved_time, template=None):
    """Calculate score based on TTA and TTR, with template expectations if available."""
    if not acknowledged_time or not resolved_time:
        return 0
    
    tta = acknowledged_time - start_time
    ttr = resolved_time - start_time
    
    # Base scoring (existing logic)
    base_score = 100
    
    # TTA penalties
    if tta <= 60:  # Under 1 minute
        tta_score = 0
    elif tta <= 300:  # Under 5 minutes
        tta_score = (tta - 60) * 0.1
    else:  # Over 5 minutes
        tta_score = (tta - 300) * 0.2 + 24
    
    # TTR penalties
    if ttr <= 300:  # Under 5 minutes
        ttr_score = 0
    elif ttr <= 1800:  # Under 30 minutes
        ttr_score = (ttr - 300) * 0.05
    else:  # Over 30 minutes
        ttr_score = (ttr - 1800) * 0.1 + 75
    
    # Template-specific scoring if available
    if template:
        expected_tta = template.get('expected_tta')
        expected_ttr = template.get('expected_ttr')
        
        if expected_tta and expected_ttr:
            # Bonus for beating expectations
            if tta <= expected_tta:
                tta_score *= 0.5  # Reduce penalty if within expected time
            if ttr <= expected_ttr:
                ttr_score *= 0.5  # Reduce penalty if within expected time
    
    final_score = max(0, base_score - tta_score - ttr_score)
    return int(final_score)

def format_summary(incident, score, template=None):
    """Format incident summary with template information if available."""
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
    # Add template information if available
    template_info = ""
    if template:
        difficulty = template.get('difficulty', 'medium')
        category = template.get('category', 'general')
        expected_tta = template.get('expected_tta')
        expected_ttr = template.get('expected_ttr')
        
        template_info = f"\n• *Template:* {difficulty.title()} difficulty, {category} category"
        if expected_tta:
            template_info += f"\n• *Expected TTA:* {expected_tta//60}m {expected_tta%60}s"
        if expected_ttr:
            template_info += f"\n• *Expected TTR:* {expected_ttr//60}m {expected_ttr%60}s"
    
    return blocks 