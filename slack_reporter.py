import os
import csv
from slack_sdk import WebClient

SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#oncall-fire-drills')
CSV_FILE = "fire_drill_scores.csv"

client = WebClient(token=SLACK_TOKEN)

def post_latest_score():
    with open(CSV_FILE, 'r') as csvfile:
        reader = list(csv.DictReader(csvfile))
        if not reader:
            print("No scores to report.")
            return
        latest = reader[-1]
        user = latest['user']
        tta = latest['tta']
        ttr = latest['ttr']
        score = latest['score']
        text = f"""\
🚨 *Fire Drill Summary*

👤 On-Call: {user}
🗱️ TTA: {tta}s | TTR: {ttr}s
🏆 Score: {score}/100

Keep up the readiness! 🔥
"""
        client.chat_postMessage(channel=SLACK_CHANNEL, text=text)
        print(f"Posted summary for {user} to Slack.")

if __name__ == "__main__":
    post_latest_score() 