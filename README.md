# 🚒 Fire Drill Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Automate on-call fire drills with PagerDuty and Slack. Random, safe, and fun!**

---

## 📋 Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Screenshots](#screenshots)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Manual Setup](#manual-setup)
- [FAQ](#faq)
- [Security](#security)
- [Contributors](#contributors)

---

## ✨ Features
- 🔥 Randomly triggers PagerDuty incidents during business hours (9am–5pm, Mon–Fri)
- 👤 Assigns to the on-call engineer
- ⏱️ Tracks time to acknowledge (TTA) and resolve (TTR)
- 🏆 Scores and reports responses
- 💬 Posts summary and interactive feedback to Slack
- 🛠️ One-command install and launch scripts

---

## 🚀 Quick Start

### 1. **Download & Install**
```sh
# Download and unzip the repo, then:
bash install.sh
```

### 2. **Configure**
```sh
cp .env.example .env
# Edit .env and fill in your PagerDuty and Slack info
```

### 3. **Start the Bot**
```sh
bash start.sh
```
- Follow the on-screen instructions to set up Slack URLs
- Add the slash command and interactivity URLs to your Slack app

### 4. **Use in Slack**
- Type `/trigger-drill` in any channel where your bot is present
- Get real-time updates and a summary with feedback buttons

---

## 🖼️ Screenshots
> _Add screenshots here!_

---

## 🗝️ How to Get Your .env Values (Step-by-Step)

### PagerDuty
- **PD_API_KEY** (PagerDuty API Access Key):
  1. Log in to PagerDuty.
  2. In the top menu, go to **Integrations > API Access Keys**.
  3. Click **Create New API Key** (choose "Read-write access").
  4. Copy the key shown and paste it in your `.env` as `PD_API_KEY`.
  5. _Reference: The API Access Keys page is under Integrations in the main navigation._

- **PD_SERVICE_ID** (Service ID):
  1. In the top menu, click **Services**.
  2. Click the name of your test service (e.g., "On Call Bot").
  3. Click **Service Settings** (gear icon or tab).
  4. Look at your browser’s address bar: the Service ID is the code after `/services/` (e.g., `PA12345`).
  5. _Reference: The Service ID is visible in the URL when viewing your service._

- **PD_USER_ID** (User ID):
  1. In the top menu, click **People**.
  2. Click your name (or the user you want to use).
  3. Click **User Settings**.
  4. Look at your browser’s address bar: the User ID is the code after `/users/` (e.g., `PABCDEF`).
  5. _Reference: The User ID is visible in the URL when viewing your user profile._

### Slack
- **SLACK_TOKEN** (Bot User OAuth Token):
  1. Go to [Slack API: Your Apps](https://api.slack.com/apps) and select your app.
  2. In the left sidebar, click **OAuth & Permissions**.
  3. Under **Scopes**, add at least these Bot Token Scopes: `chat:write`, `commands`, `channels:read` (and `groups:read` for private channels).
  4. At the top of the OAuth & Permissions page, click **Install App to Workspace** (or **Reinstall** if already installed).
  5. After installation, you’ll see **Bot User OAuth Token** (starts with `xoxb-...`).
  6. Copy this token and paste it in your `.env` as `SLACK_TOKEN`.
  7. _Reference: This is NOT the Client Secret or Signing Secret. It is the Bot User OAuth Token shown after installing the app._

- **SLACK_SIGNING_SECRET** (Signing Secret):
  1. In your Slack app settings, click **Basic Information** in the left sidebar.
  2. Scroll down to **App Credentials**.
  3. Click **Show** next to **Signing Secret**.
  4. Copy this value and paste it in your `.env` as `SLACK_SIGNING_SECRET`.
  5. _Reference: The Signing Secret is in the App Credentials section of Basic Information._

- **SLACK_CHANNEL** (optional):
  1. Use the Slack channel name (e.g., `#oncall-fire-drills`).
  2. If not set, defaults to `#oncall-fire-drills`.
  3. The bot must be invited to this channel.

---

## ⚙️ How It Works
1. **Random Fire Drill**: Bot triggers a PagerDuty incident at random during business hours
2. **On-Call Assignment**: Assigns to the current on-call engineer
3. **Slack Updates**: Posts incident status and summary to Slack
4. **Scoring**: Tracks TTA/TTR and scores the response
5. **Feedback**: Users can give instant feedback via Slack buttons

---

## 🛠️ Configuration
- `.env` file holds all secrets (see `.env.example`)
- All scripts and code are at the repo root for easy access
- No coding required to use

---

## 🛠️ Manual Setup (for reference)
See the full instructions in the README below if you want to set up manually or customize further.

---

## ❓ FAQ
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

## 👥 Contributors
- [@sidverma-pd](https://github.com/sidverma-pd)

---

## 🏁 You’re Ready!
- Run `/trigger-drill` in Slack and watch the magic happen! 