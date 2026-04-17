#!/bin/bash
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install requests > /dev/null 2>&1

echo "Starting Polymarket Daemon..."
# Run the bot in the background
python polymarket_bot.py &
BOT_PID=$!

echo "Starting Web Server on port 8080..."
echo "Access the dashboard at http://localhost:8080"
# Run the server in foreground
python -m http.server 8080

# If the server is killed with Ctrl+C, also kill the bot
trap "kill $BOT_PID" EXIT
