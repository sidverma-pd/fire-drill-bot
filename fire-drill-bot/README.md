# Fire Drill Bot

A simulated on-call fire drill bot for PagerDuty and Slack. Randomly triggers safe incidents, tracks response times, and posts weekly scores to Slack.

---

## 🚀 Quick Start (No Coding Required)

### 1. Download & Install

1. **Download the bot files:**
   - Click the green "Code" button on GitHub, then "Download ZIP".
   - Unzip the file to your computer (e.g., Desktop).
2. **Open a Terminal/Command Prompt:**
   - On Mac: Open "Terminal" (search in Spotlight).
   - On Windows: Open "Command Prompt" (search in Start Menu).
3. **Go to the bot folder:**
   - Type: `cd Desktop/fire-drill-bot` (or wherever you unzipped it)
4. **Run the installer:**
   - Type:
     ```sh
     bash install.sh
     ```
   - This will install everything you need (Python, dependencies, ngrok).

### 2. Set Up Your Accounts

- **PagerDuty:**
  - Create a test service and API key (see below for details)
- **Slack:**
  - Create a Slack app and bot token (see below for details)

### 3. Configure the Bot

1. **Copy the example environment file:**
   ```sh
   cp .env.example .env
   ```
2. **Edit `.env` with your info:**
   - Open `.env` in a text editor (double-click it)
   - Fill in your PagerDuty and Slack info (see comments in the file)

### 4. Start the Bot

1. **Run the bot:**
   ```sh
   bash start.sh
   ```
2. **Follow the on-screen instructions:**
   - The bot will guide you to set up ngrok and Slack URLs
   - You’ll see a link to add the slash command to Slack

### 5. Use in Slack

- In Slack, type `/trigger-drill` in any channel where your bot is present
- You’ll get real-time updates and a summary with feedback buttons

---

## 📦 What’s Included
- `install.sh` — One-command installer for all dependencies
- `start.sh` — One-command launcher for the bot and ngrok
- `.env.example` — Example config file for your secrets
- `README.md` — This guide
- All bot code (no coding required to use)

---

## 🛠️ Manual Setup (for reference)

## Features
- **Randomly triggers PagerDuty incidents** during business hours (9am–5pm, Mon–Fri)
- **Assigns to the on-call engineer**
- **Tracks time to acknowledge (TTA) and resolve (TTR)**
- **Scores and reports responses**
- **Posts summary to Slack**

---

## Prerequisites
- **PagerDuty account** (REST API v2, test service, escalation policy)
- **Slack workspace** and bot token
- **AWS account** (Lambda, EventBridge)
- **Python 3.8+**

---

## 1. PagerDuty Setup

### a. Create a Test Service
1. Go to PagerDuty: `Configuration > Services > New Service`
2. Name it something like `Fire Drill Service`
3. Attach an escalation policy with real on-call users
4. Label it clearly (e.g., tag or name: `test/fire-drill`)

### b. Get Service and User IDs
- **Service ID:**
  - In the PagerDuty UI, go to your service, click "Settings". The Service ID is in the URL or under "API".
  - Or use the API: `GET /services`
- **User ID:**
  - Go to `People > Users`, click the user, and copy the User ID from the URL or API.

### c. Create a PagerDuty API Key
1. Go to `Configuration > API Access Keys`
2. Click "Create New API Key"
3. Choose "Read-write access"
4. Save the key securely

---

## 2. AWS Lambda Setup

### a. Prepare the Lambda Function
1. Copy `lambda_function.py` to your local machine
2. Install dependencies locally:
   ```sh
   pip install -r requirements.txt -t ./package
   cp lambda_function.py ./package/
   cd package
   zip -r ../fire-drill-lambda.zip .
   cd ..
   ```

### b. Deploy to AWS Lambda
1. Go to AWS Lambda Console
2. Create a new function (Python 3.8+)
3. Upload `fire-drill-lambda.zip` as the function code
4. Set environment variables:
   - `PD_API_KEY`: PagerDuty API key
   - `PD_SERVICE_ID`: PagerDuty Service ID
   - `PD_USER_ID`: PagerDuty User ID (on-call)
5. Set the handler to `lambda_function.lambda_handler`
6. Set timeout to at least 30 seconds

### c. Schedule with EventBridge
1. Go to EventBridge (CloudWatch Events)
2. Create a new rule:
   - **Schedule expression:**
     - For 10am–4pm PT, Mon–Fri (in UTC):
       ```
       cron(0/60 17-23 ? * MON-FRI *)
       ```
   - Attach the rule to your Lambda function

---

## 3. Scoring & Reporting

### a. Track and Score Responses
1. Run `score_tracker.py` locally or as a scheduled job (e.g., weekly):
   ```sh
   export PD_API_KEY=...  # Your PagerDuty API key
   export PD_SERVICE_ID=...  # Your PagerDuty Service ID
   python score_tracker.py
   ```
2. This will create/update `fire_drill_scores.csv` with incident scores.

### b. Post Scoreboard to Slack
1. Create a Slack bot and get a bot token ([guide](https://api.slack.com/authentication/basics))
2. Invite the bot to your desired channel (e.g., `#oncall-fire-drills`)
3. Run `slack_reporter.py`:
   ```sh
   export SLACK_TOKEN=...  # Your Slack bot token
   export SLACK_CHANNEL=#oncall-fire-drills  # (optional, default is #oncall-fire-drills)
   python slack_reporter.py
   ```
4. The script will post the latest fire drill score to Slack.

---

## 4. Environment Variables

| Variable         | Purpose                        | Where to set           |
|------------------|-------------------------------|------------------------|
| PD_API_KEY       | PagerDuty API key              | Lambda, local scripts  |
| PD_SERVICE_ID    | PagerDuty Service ID           | Lambda, local scripts  |
| PD_USER_ID       | PagerDuty User ID (on-call)    | Lambda                 |
| SLACK_TOKEN      | Slack Bot token                | Local scripts          |
| SLACK_CHANNEL    | Slack channel (e.g. #oncall-fire-drills) | Local scripts |

---

## 5. Requirements

Install Python dependencies:
```sh
pip install -r requirements.txt
```

---

## 6. Usage Summary

- **Incident Triggering:**
  - Lambda function runs on schedule, randomly triggers a fire drill incident in PagerDuty during business hours.
- **Scoring:**
  - Run `score_tracker.py` to fetch incidents, calculate TTA/TTR, and score responses. Results are saved to CSV.
- **Slack Reporting:**
  - Run `slack_reporter.py` to post the latest score to Slack.

---

## 7. Troubleshooting & Tips

- **No incidents created?**
  - Check Lambda logs for errors
  - Ensure business hours and random skip logic (60% of runs will skip by default)
  - Confirm environment variables are set correctly
- **No scores in CSV?**
  - Ensure incidents are labeled with "🔥 Fire Drill"
  - Check PagerDuty API permissions
- **Slack message not posting?**
  - Confirm bot is invited to the channel
  - Check Slack token and permissions
- **Testing Locally:**
  - You can run `lambda_function.py` locally by setting the environment variables and calling `lambda_handler({}, None)`

---

## 8. Safety & Best Practices

- Use only test services and label incidents clearly
- Ensure drill incidents do not impact SLO metrics
- Get team buy-in before public reporting
- Rotate API keys and tokens regularly

---

## 9. Optional Enhancements

- Add a `/trigger-drill` Slack command
- Use PagerDuty's `GET /oncalls` API to auto-assign the current on-call
- Store results in DynamoDB or another database
- Build a Grafana dashboard from results
- Auto-create Jira tickets for missed drills

---

## 10. File Overview

- `lambda_function.py` — AWS Lambda function to trigger PagerDuty incidents
- `score_tracker.py` — Script to fetch, score, and log fire drill responses
- `slack_reporter.py` — Script to post the latest score to Slack
- `requirements.txt` — Python dependencies
- `README.md` — This documentation

---

## 11. Example Workflow

1. **Deploy Lambda** to AWS and schedule with EventBridge
2. **Run scoring script** weekly (manually or via cron)
3. **Post results to Slack** with the reporter script

---

## 12. Support

For questions or improvements, open an issue or PR! 

---

## 13. Slack Integration: Slash Command & Real-Time Updates

### a. Running the Slack App

1. Install additional requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `SLACK_TOKEN`: Slack Bot token
   - `SLACK_SIGNING_SECRET`: Slack app signing secret
   - `SLACK_CHANNEL`: Slack channel (e.g. #oncall-fire-drills)
   - `PD_API_KEY`, `PD_SERVICE_ID`, `PD_USER_ID`: PagerDuty credentials
3. Start the Flask app:
   ```sh
   python slack_app.py
   ```
4. Expose your Flask app to the internet (for Slack to reach it) using a tool like [ngrok](https://ngrok.com/):
   ```sh
   ngrok http 5000
   ```
5. Copy the public URL from ngrok (e.g., `https://xxxx.ngrok.io`)

### b. Set Up the Slack Slash Command

1. Go to your Slack app settings at https://api.slack.com/apps
2. Add a new Slash Command (e.g., `/trigger-drill`)
3. Set the Request URL to: `https://xxxx.ngrok.io/slack/command`
4. Save changes and reinstall the app to your workspace if needed

### c. Usage

- In any Slack channel where your bot is present, type `/trigger-drill` to trigger a fire drill.
- The bot will:
  - Trigger a PagerDuty incident (during business hours)
  - Post a confirmation and incident ID to the channel
  - (Planned) Post real-time updates and a final report when the incident is closed

--- 

---

## 📝 FAQ

**Q: Do I need to know Python or code?**
A: No! Just follow the steps above and copy-paste commands.

**Q: What if I get stuck?**
A: Ask your team’s tech lead or open an issue on GitHub for help.

**Q: Is this safe for production?**
A: Use only with test services and get team buy-in before public reporting.

---

## 🔒 Security
- Never share your `.env` file or API keys
- Use only test services for drills

---

## 🏁 You’re Ready!
- Run `/trigger-drill` in Slack and watch the magic happen!

--- 