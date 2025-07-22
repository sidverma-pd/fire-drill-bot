#!/bin/bash
set -e

source venv/bin/activate

# Start Flask app in background
export FLASK_APP=slack_app.py
export FLASK_ENV=production
nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
FLASK_PID=$!

# Start ngrok
nohup venv/bin/ngrok http 5000 > ngrok.log 2>&1 &
sleep 3
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[a-zA-Z0-9\-]*\.ngrok.io' | head -n 1)

if [ -z "$NGROK_URL" ]; then
  echo "Could not get ngrok URL. Is ngrok running?"
  exit 1
fi

echo "\n🚀 Fire Drill Bot is running!"
echo "- Slack command URL: $NGROK_URL/slack/command"
echo "- Slack interactivity URL: $NGROK_URL/slack/interactivity"
echo "- To stop the bot: kill $FLASK_PID and killall ngrok"
echo "- To see logs: tail -f flask.log" 