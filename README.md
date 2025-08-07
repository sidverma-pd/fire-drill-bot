# 🔥 Fire Drill Bot

A Slack-integrated fire drill bot that creates realistic PagerDuty incidents for on-call training. Trigger fire drills from Slack, monitor response times, and get detailed performance reports.

## 📋 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Detailed Setup](#-detailed-setup)
- [How to Use](#-how-to-use)
- [Fire Drill Templates](#-fire-drill-templates)
- [What the Summary Shows](#-what-the-summary-shows)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)

## 🎯 Overview

The Fire Drill Bot helps teams practice their on-call response by:
- **Triggering realistic incidents** in PagerDuty from Slack
- **Monitoring response times** (Time to Acknowledge & Time to Resolve)
- **Providing detailed reports** with scoring and feedback
- **Supporting custom templates** for team-specific scenarios

### Features
- ✅ Slack integration with slash commands
- ✅ Real-time incident monitoring
- ✅ Performance scoring and reporting
- ✅ Template-based realistic scenarios
- ✅ Custom template creation
- ✅ Interactive feedback system

## 🚀 Quick Start

### For Non-Coders (One-Command Setup)

1. **Install everything:**
   ```bash
   bash install.sh
   ```

2. **Start the bot:**
   ```bash
   bash start.sh
   ```

3. **In a new terminal, start ngrok:**
   ```bash
   ngrok http 5050
   ```

4. **Copy the ngrok URL** (e.g., `https://abc123.ngrok-free.app`) and update your Slack app settings

5. **Set up your environment variables** (see Detailed Setup below)

6. **Use the bot in Slack:**
   ```
   /trigger-drill
   /trigger-template cpu_spike
   /list-templates
   ```

## ⚙️ Detailed Setup

### Prerequisites
- Python 3.7+
- PagerDuty account
- Slack workspace with admin permissions

### Step 1: Get Your Environment Variables

Create a `.env` file with these values:

```env
# PagerDuty
PD_API_KEY=your_pagerduty_api_key_here
PD_SERVICE_ID=your_pagerduty_service_id_here
PD_USER_ID=your_pagerduty_user_id_here

# Slack
SLACK_TOKEN=your_slack_bot_token_here
SLACK_SIGNING_SECRET=your_slack_signing_secret_here
SLACK_CHANNEL=#oncall-fire-drills
```

#### Getting PagerDuty Values

**PD_API_KEY:**
1. Go to PagerDuty → Integrations → API Access Keys
2. Click "Create New API Key"
3. Name it "Fire Drill Bot"
4. **Do NOT check "Read-only access"**
5. Copy the generated key

**PD_SERVICE_ID:**
1. Go to PagerDuty → Services
2. Click on your service (or create one)
3. Copy the Service ID from the URL or service details

**PD_USER_ID:**
1. Go to PagerDuty → Users
2. Click on your user profile
3. Copy the User ID from the URL or profile details

#### Getting Slack Values

**SLACK_TOKEN (Bot User OAuth Token):**
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app or select existing "Fire Drill Bot"
3. Go to "OAuth & Permissions"
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

**SLACK_SIGNING_SECRET:**
1. In your Slack app settings
2. Go to "Basic Information"
3. Copy the "Signing Secret"

**SLACK_CHANNEL (optional):**
- Defaults to `#oncall-fire-drills` if not set
- Can be any channel where the bot is invited

### Step 2: Install and Start

1. **Install dependencies:**
   ```bash
   bash install.sh
   ```

2. **Start the Flask app:**
   ```bash
   bash start.sh
   ```

3. **Start ngrok in a new terminal:**
   ```bash
   ngrok http 5050
   ```

4. **Copy the ngrok URL** (e.g., `https://abc123.ngrok-free.app`)

### Step 3: Configure Slack App

1. **Go to your Slack app settings:**
   - Visit [api.slack.com/apps](https://api.slack.com/apps)
   - Click on your "Fire Drill Bot" app

2. **Add Slash Commands:**
   - In the left sidebar, click "Slash Commands"
   - Click "Create New Command" for each:

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

3. **Add Interactivity:**
   - Go to "Interactivity & Shortcuts"
   - Turn on Interactivity
   - Request URL: `https://your-ngrok-url.ngrok-free.app/slack/interactivity`

4. **Install the app:**
   - Go to "Install App" in the left sidebar
   - Click "Install to Workspace"
   - Grant permissions when prompted

5. **Invite the bot to your channel:**
   ```
   /invite @Fire Drill Bot
   ```

## 🎮 How to Use

### Available Commands

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

## 🎯 Fire Drill Templates

The bot supports **template-based fire drills** for more realistic scenarios:

### Built-in Templates

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

### Template Features

- **Realistic scenarios** with detailed descriptions
- **Difficulty levels** (easy, medium, hard)
- **Categories** (database, infrastructure, network, etc.)
- **Expected response times** for better scoring
- **Template-specific scoring** that considers expected vs actual performance

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

## 📊 What the Summary Shows

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

## 🔧 Troubleshooting

### Common Issues

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

**PagerDuty API errors?**
- Verify your API key has write permissions (not read-only)
- Check that Service ID and User ID are correct
- Ensure the service is active in PagerDuty

**SSL Certificate errors?**
- Run: `/Applications/Python\ 3.x/Install\ Certificates.command`
- Or: `pip install --upgrade certifi`

### Getting Help

1. **Check logs:** `tail -f flask.log`
2. **Verify environment:** Ensure all `.env` variables are set
3. **Test PagerDuty API:** Try the test in the setup instructions
4. **Restart services:** Stop and restart Flask and ngrok

## ❓ FAQ

**Q: Can I use this without coding knowledge?**
A: Yes! The Quick Start section provides one-command setup and usage.

**Q: Do I need to create a new PagerDuty service?**
A: You can use an existing service or create a new one specifically for fire drills.

**Q: Can I customize the fire drill scenarios?**
A: Yes! See the "Creating Custom Templates" section for detailed instructions.

**Q: How does the scoring work?**
A: Scores are based on Time to Acknowledge (TTA) and Time to Resolve (TTR), with bonuses for beating template expectations.

**Q: Can I run multiple fire drills at once?**
A: Yes, the bot can handle multiple concurrent incidents.

**Q: Is this secure?**
A: Yes, all API keys are stored locally in `.env` files (not committed to git).

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the fire drill bot!

## 📄 License

This project is open source and available under the MIT License. 