# Speedy: A simple alpha bot for Polymarket

Speedy is a tool I built to cut through the noise on Polymarket. It scans active events and flags high-liquidity crypto markets (mostly BTC and ETH) that actually have enough volume and tight spreads to be worth trading.

---

## 🏗️ How it works

The setup is pretty straightforward. It's split into two main parts:

1.  **The Backend (Python)**: This is the "daemon" (`polymarket_bot.py`). It hits the Polymarket Gamma API every 15 seconds, filters out all the sports/politics junk, and runs a quick scoring script to see which markets are heating up. It saves everything into `signals.json`.
2.  **The Dashboard (Web)**: A clean UI that pulls from that JSON file. It shows a quick heatmap of what's moving in crypto and a feed of "active" signals you can click through to trade.

---

## ✨ What it does

*   **Crypto only**: It's hard-coded to ignore politics, sports, and random news events. If it's not crypto-related, it won't show up.
*   **Smart scoring**: It looks at depth (liquidity), daily volume, and the bid-ask spread. If a market is too thin or the spread is massive, it gets buried.
*   **Momentum alerts**: It flags markets that are moving fast in the last hour.
*   **Simulation mode**: There's a toggle in the UI that lets you see where the bot "would" have entered a trade without actually putting money down.
*   **No fluff UI**: Built with a clean, professional aesthetic so it looks good on a second monitor.

---

## 🔄 The Workflow

It's a loop that looks like this:
- The Python bot wakes up and grabs the top 300 events.
- It calculates a "Tradability Score" from 0 to 100.
- Markets with a score over 70 get boosted to the top of the feed.
- The UI refreshes every 5 seconds to stay in sync with the bot's data.

---

## 🚀 Getting Started

### Prerequisites
You'll just need Python 3.8+ and an internet connection.

### 1. The Easy Way
I've included a `run.sh` script that sets up a virtual environment, installs the `requests` library, and fires up both the bot and a local web server at once.
```bash
chmod +x run.sh
./run.sh
```
Then just open [http://localhost:8080](http://localhost:8080) in your browser.

### 2. Manual Setup
If you want to run things yourself:

**Run the bot:**
```bash
pip install requests
python3 polymarket_bot.py
```

**Run the dashboard:**
```bash
# In a new terminal
python3 -m http.server 8080
```

---

## 📊 The "Tradability" Score
I use a mix of three things to decide if a market is "good":
- **Liquidity (35%)**: Is there enough depth to get in and out?
- **Volume (35%)**: Are people actually trading this right now?
- **Spread (30%)**: How much are you losing to the "gap"?

If a market is specifically about BTC or ETH, it gets a 1.5x multiplier because that's what this bot is optimized for.

---
*Built for fast execution and spotting crypto alpha.*
