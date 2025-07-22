#!/bin/bash

source venv/bin/activate

# Start Flask app in background
export FLASK_APP=slack_app.py
export FLASK_ENV=production
nohup flask run --host=0.0.0.0 --port=5050 > flask.log 2>&1 &
FLASK_PID=$!

echo -e "\n🚀 Fire Drill Bot Flask app is running in the background!"
echo "- To see logs: tail -f flask.log"
echo "- To stop the bot: kill $FLASK_PID"
echo -e "\n👉 In a new terminal, run: ngrok http 5050"
echo "   Then update your Slack URLs as follows:"
echo "   Slack Command URL: <ngrok-url>/slack/command"
echo "   (e.g., if ngrok gives https://abc123.ngrok-free.app, use https://abc123.ngrok-free.app/slack/command)"
echo "   Update these at: api.slack.com -> Your Apps -> Fire Drill Bot -> Slash Command" 