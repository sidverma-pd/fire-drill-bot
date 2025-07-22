# 🚒 Fire Drill Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Automated, interactive on-call fire drill bot for PagerDuty and Slack.**

---

## 📦 Project Overview

Fire Drill Bot helps your team practice incident response by simulating realistic outages. Trigger drills on demand from Slack, track response metrics, and get instant feedback—all with a modern, modular Python codebase.

---

## 🏗️ Architecture

- **slack_app.py**: Flask app, Slack command & interactivity endpoints
- **incident_titles.py**: 100+ realistic fire drill scenarios (with urgency)
- **pagerduty_client.py**: PagerDuty API integration (trigger, poll)
- **slack_client.py**: Slack API integration (messages, feedback)
- **incident_logic.py**: Polling, scoring, and summary formatting

```
Slack /trigger-drill
   │
   ▼
slack_app.py ──▶ pagerduty_client.py ──▶ PagerDuty
   │
   ├─▶ incident_titles.py (random scenario)
   │
   ├─▶ incident_logic.py (polls, scores, formats)
   │
   └─▶ slack_client.py (posts updates/summary)
```

---

## 🚀 Quick Start

1. **Clone the repo & install dependencies:**
   ```sh
   git clone <repo-url>
   cd fire-drill-bot
   bash install.sh
   pip install -r requirements.txt
   ```
2. **Set up your `.env` file:**
   ```sh
   cp .env.example .env
   # Edit .env and fill in your PagerDuty and Slack info
   ```
3. **Start Flask:**
   ```sh
   export FLASK_APP=slack_app.py
   flask run --host=0.0.0.0 --port=5050
   ```
4. **Start ngrok manually in a new terminal:**
   ```sh
   ngrok http 5050
   ```
   - Copy the HTTPS URL from the ngrok output (e.g., `https://abc12345.ngrok-free.app`)
5. **Update your Slack app:**
   - Set your Slash Command Request URL to: `<ngrok-url>/slack/command`
   - Set your Interactivity URL to: `<ngrok-url>/slack/interactivity`
   - Add required bot token scopes: `chat:write`, `commands`, etc.
   - Install the app to your workspace
6. **Trigger a drill in Slack:**
   - Type `/trigger-drill` in any channel where your bot is present

---

## 🗝️ Environment Variables

See `.env.example` for all required variables. Key ones:
- `PD_API_KEY`: PagerDuty API key (**do NOT check 'Read-only access'**)
- `PD_SERVICE_ID`: PagerDuty Service ID
- `PD_USER_ID`: PagerDuty User ID
- `SLACK_TOKEN`: Slack Bot User OAuth Token (starts with `xoxb-...`)
- `SLACK_SIGNING_SECRET`: Slack app signing secret
- `SLACK_CHANNEL`: (optional) Slack channel for notifications

---

## ✨ Features
- 100+ realistic, randomly selected fire drill scenarios (with urgency)
- Trigger drills on demand from Slack with `/trigger-drill`
- Real-time updates: triggered, acknowledged, resolved, summary
- Tracks TTA (Time to Acknowledge), TTR (Time to Resolve), and scores
- Interactive Slack feedback buttons
- Modular, extensible Python codebase

---

## 🛠️ Extending & Customizing
- **Add more scenarios:** Edit `incident_titles.py`
- **Change scoring/reporting:** Edit `incident_logic.py`
- **Integrate with other tools:** Add new modules or Slack actions

---

## 🧑‍💻 Troubleshooting
- **SSL errors on macOS:** Run `/Applications/Python\ 3.x/Install\ Certificates.command`
- **401 from PagerDuty:** Double-check your API key and permissions
- **No Slack response:** Make sure your ngrok URL is correct and Flask is running
- **Env vars not loading:** Use `python-dotenv` and restart Flask after changes

---

## 🙌 Contributors
- [@sidverma-pd](https://github.com/sidverma-pd)

---

## 🏁 You’re Ready!
- Run `/trigger-drill` in Slack and watch your team level up their incident response! 