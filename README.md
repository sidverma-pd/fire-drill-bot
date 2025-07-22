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

## 🗝️ How to Get Your .env Values

### PagerDuty
- **PD_API_KEY**: 
  1. Log in to PagerDuty.
  2. Go to **Configuration > API Access Keys**.
  3. Click **Create New API Key** (choose "Read-write access").
  4. Copy the key and paste it in your `.env`.
- **PD_SERVICE_ID**:
  1. Go to **Configuration > Services** and select your test service.
  2. The Service ID is in the URL (after `/services/`) or under the service's settings/API tab.
- **PD_USER_ID**:
  1. Go to **People > Users** and click your user.
  2. The User ID is in the URL (after `/users/`).

### Slack
- **SLACK_TOKEN**:
  1. Go to [Slack API: Your Apps](https://api.slack.com/apps) and select your app (or create one).
  2. Under **OAuth & Permissions**, install the app to your workspace.
  3. Copy the **Bot User OAuth Token** (starts with `xoxb-`).
- **SLACK_SIGNING_SECRET**:
  1. In your Slack app settings, go to **Basic Information**.
  2. Copy the **Signing Secret**.
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