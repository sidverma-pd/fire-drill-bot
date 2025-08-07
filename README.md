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
3. **Start the bot:**
   ```sh
   bash start.sh
   ```
   - This will start Flask in the background and print instructions for running ngrok and updating your Slack URLs.
4. **In a new terminal, run ngrok:**
   ```sh
   ngrok http 5050
   ```
   - Copy the HTTPS URL from the ngrok output (e.g., `https://abc12345.ngrok-free.app`)
5. **Update your Slack app URLs:**
   - Go to [api.slack.com](https://api.slack.com/) → Your Apps → Fire Drill Bot
   - Under **Slash Commands**, set the Request URL to: `<ngrok-url>/slack/command`
   - Under **Interactivity & Shortcuts**, set the Request URL to: `<ngrok-url>/slack/interactivity`
   - (e.g., if ngrok gives `https://abc12345.ngrok-free.app`, use `https://abc12345.ngrok-free.app/slack/command`)
   - **Note:** If you restart ngrok, the URL will change. Always update your Slack app with the new URL!
6. **Trigger a drill in Slack:**
   - Type `/trigger-drill` in any channel where your bot is present

---

## 🎯 Fire Drill Templates

The bot supports **template-based fire drills** for more realistic scenarios:

### Available Commands:
- `/trigger-drill` - Random fire drill (original behavior)
- `/trigger-template <template_name>` - Run a specific template
- `/list-templates` - See all available templates

### Built-in Templates:
- **database_connection_failure** - Database connection pool exhausted
- **cpu_spike** - CPU usage at 95% on production servers  
- **memory_leak** - Memory leak in application pods
- **network_latency** - High latency between regions
- **disk_space** - Disk space at 95% on critical servers
- **api_rate_limit** - External API rate limit exceeded
- **ssl_certificate** - SSL certificate expiring soon
- **cache_miss** - Redis cache cluster down
- **load_balancer** - Load balancer health checks failing
- **database_deadlock** - Database deadlock causing failures

### Template Features:
- **Realistic scenarios** with detailed descriptions
- **Difficulty levels** (easy, medium, hard)
- **Categories** (database, infrastructure, network, etc.)
- **Expected response times** for better scoring
- **Template-specific scoring** that considers expected vs actual performance

### Example Usage:
```
/trigger-template cpu_spike
/trigger-template database_connection_failure
/trigger-template memory_leak
```

### Creating Custom Templates

You can create your own fire drill templates to simulate scenarios specific to your team.

#### Template Format

Templates are defined in `fire_drill_templates.py` using this format:

```python
"your_template_name": {
    "title": "🔥 Fire Drill: [Your Scenario Description]",
    "urgency": "high",  # low, high, or critical
    "description": "Detailed description of what's happening...",
    "expected_tta": 300,  # Expected time to acknowledge (seconds)
    "expected_ttr": 1800,  # Expected time to resolve (seconds)
    "difficulty": "medium",  # easy, medium, or hard
    "category": "your_category"  # database, infrastructure, network, etc.
}
```

#### Required Fields

- **title**: The incident title that appears in PagerDuty
- **urgency**: How urgent the incident is (affects PagerDuty priority)
- **description**: Detailed description of what's happening

#### Optional Fields

- **expected_tta**: Expected time to acknowledge in seconds
- **expected_ttr**: Expected time to resolve in seconds  
- **difficulty**: How challenging the scenario is
- **category**: What type of incident this is

#### Step-by-Step: Adding Your Template

1. **Open the template file:**
   ```bash
   nano fire_drill_templates.py
   ```

2. **Add your template to the `FIRE_DRILL_TEMPLATES` dictionary:**
   ```python
   "payment_processor_down": {
       "title": "🔥 Fire Drill: Payment processor API completely down",
       "urgency": "critical",
       "description": "Third-party payment processor is returning 500 errors for all requests. No payments can be processed and customers are getting errors during checkout.",
       "expected_tta": 120,  # 2 minutes
       "expected_ttr": 900,  # 15 minutes
       "difficulty": "hard",
       "category": "integration"
   }
   ```

3. **Restart the Flask app:**
   ```bash
   # Stop the current app
   pkill -f "flask run"
   
   # Start it again
   bash start.sh
   ```

4. **Test your template:**
   ```
   /trigger-template payment_processor_down
   ```

#### Template Categories

- **database**: Database-related issues
- **infrastructure**: Server, CPU, memory issues
- **network**: Connectivity, latency issues
- **application**: Code, deployment issues
- **integration**: Third-party API issues
- **security**: SSL, authentication issues
- **general**: Other scenarios

#### Difficulty Levels

- **easy**: Simple issues that should be resolved quickly
- **medium**: Standard issues with moderate complexity
- **hard**: Complex issues requiring investigation and coordination

#### Scoring Impact

Templates with `expected_tta` and `expected_ttr` values will:
- Reduce scoring penalties if teams respond within expected times
- Provide more realistic performance expectations
- Help teams understand what "good" response times look like

#### Best Practices

1. **Be realistic**: Base scenarios on real incidents your team has faced
2. **Vary difficulty**: Include easy, medium, and hard scenarios
3. **Set expectations**: Use expected_tta/ttr to define reasonable response times
4. **Be specific**: Detailed descriptions help teams understand the scenario
5. **Test regularly**: Update templates based on team feedback and performance

For more detailed template creation guidance, see `TEMPLATE_GUIDE.md`.

---

## 🚀 How to Trigger Fire Drills in Slack

Once your bot is running, you can trigger fire drills directly from Slack using slash commands.

### Setting Up Slack Commands

1. **Go to your Slack App settings:**
   - Visit [api.slack.com/apps](https://api.slack.com/apps)
   - Click on your "Fire Drill Bot" app

2. **Add Slash Commands:**
   - In the left sidebar, click "Slash Commands"
   - Click "Create New Command"
   - Add these three commands:

   **Command 1:**
   - Command: `/trigger-drill`
   - Request URL: `https://your-ngrok-url.ngrok-free.app/slack/command`
   - Short Description: `Trigger a random fire drill`
   - Usage Hint: `Just type /trigger-drill`

   **Command 2:**
   - Command: `/trigger-template`
   - Request URL: `https://your-ngrok-url.ngrok-free.app/slack/command`
   - Short Description: `Trigger a specific fire drill template`
   - Usage Hint: `/trigger-template <template_name>`

   **Command 3:**
   - Command: `/list-templates`
   - Request URL: `https://your-ngrok-url.ngrok-free.app/slack/command`
   - Short Description: `List all available fire drill templates`
   - Usage Hint: `Just type /list-templates`

3. **Save and Install:**
   - Click "Save" for each command
   - Go to "Install App" in the left sidebar
   - Click "Install to Workspace"
   - Grant permissions when prompted

### Using the Commands

#### Random Fire Drill
```
/trigger-drill
```
Triggers a random fire drill scenario. The bot will:
- Create a PagerDuty incident
- Post the incident details to your Slack channel
- Monitor the incident and provide updates
- Post a final summary with scoring

#### Template-Based Fire Drill
```
/trigger-template cpu_spike
/trigger-template database_connection_failure
/trigger-template memory_leak
```
Triggers a specific, realistic scenario. The bot will:
- Create a PagerDuty incident with detailed description
- Post template information (difficulty, category, expected times)
- Monitor and provide updates
- Score based on template expectations

#### List Available Templates
```
/list-templates
```
Shows all available fire drill templates with their categories and difficulty levels.

### What Happens When You Trigger a Drill

1. **Immediate Response:** The bot confirms the drill was triggered and shows the incident ID
2. **Slack Notification:** A message is posted to your channel with incident details
3. **Real-time Updates:** The bot monitors the incident and posts updates:
   - When someone acknowledges the incident
   - When someone resolves the incident
4. **Final Summary:** A detailed summary is posted with:
   - Response times (TTA/TTR)
   - Performance score
   - Template information (if applicable)
   - Feedback buttons

### Example Workflow

1. **Trigger:** Type `/trigger-template cpu_spike` in Slack
2. **Notification:** Bot posts: "🚨 Template fire drill triggered by @user: CPU usage at 95% on production servers"
3. **Monitoring:** Bot watches for acknowledgment and resolution
4. **Updates:** Bot posts when incident is acknowledged/resolved
5. **Summary:** Bot posts final report with scoring and feedback options

### Troubleshooting

**Command not working?**
- Check that your ngrok URL is correct in the Slack app settings
- Ensure the Flask app is running (`bash start.sh`)
- Verify ngrok is running (`ngrok http 5050`)

**No response from bot?**
- Check the Flask logs: `tail -f flask.log`
- Verify your Slack bot token and signing secret are correct
- Make sure the bot is invited to the channel where you're using the command

**Commands not showing up?**
- Make sure you've installed the app to your workspace
- Check that the Request URLs are correct (include `/slack/command`)
- Try reinstalling the app if needed

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

## 📊 What Does the Slack Summary Show?

After each fire drill, the bot posts a summary in Slack with:
- **On-Call:** Who was assigned the incident
- **Incident ID:** PagerDuty incident identifier
- **Created:** When the incident was triggered
- **Acknowledged:** When and by whom the incident was acknowledged (or 'Not acknowledged')
- **Resolved:** When and by whom the incident was resolved (or 'Not resolved')
- **TTA (Time to Acknowledge):** Seconds from trigger to acknowledge (if acknowledged)
- **TTR (Time to Resolve):** Seconds from trigger to resolve (if resolved)
- **Score:** Calculated based on TTA and TTR
- **Feedback buttons:** Users can give instant feedback on the drill

This helps your team track readiness, response speed, and gather feedback for continuous improvement.

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