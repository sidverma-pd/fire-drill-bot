#!/bin/bash
set -e

# Check for Python 3
if ! command -v python3 &> /dev/null; then
  echo "Python 3 is required. Please install Python 3 and rerun this script."
  exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null; then
  echo "pip3 is required. Please install pip3 and rerun this script."
  exit 1
fi

# Install virtualenv if not present
if ! python3 -m virtualenv --version &> /dev/null; then
  pip3 install virtualenv
fi

# Create virtual environment
python3 -m virtualenv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Download ngrok if not present
if ! command -v ngrok &> /dev/null; then
  echo "Downloading ngrok..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    curl -s https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip -o ngrok.zip
  else
    curl -s https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -o ngrok.zip
  fi
  unzip ngrok.zip
  chmod +x ngrok
  mv ngrok venv/bin/
  rm ngrok.zip
fi

echo "\n✅ Install complete!"
echo "Next steps:"
echo "1. Copy .env.example to .env and fill in your PagerDuty and Slack info."
echo "2. Run 'bash start.sh' to launch the bot."
echo "3. Follow the on-screen instructions." 