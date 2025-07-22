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

// ... (rest of the detailed setup instructions as previously provided) ...

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