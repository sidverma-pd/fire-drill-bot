import os
from slack_sdk import WebClient

SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#oncall-fire-drills')

client = WebClient(token=SLACK_TOKEN)

def post_message(text=None, blocks=None):
    client.chat_postMessage(channel=SLACK_CHANNEL, text=text, blocks=blocks)

def post_feedback_response(user, action):
    text = f"Thank you <@{user}> for your feedback: *{action}*."
    client.chat_postMessage(channel=SLACK_CHANNEL, text=text) 