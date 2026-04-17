# speedy

a polymarket scanner for crypto markets worth trading. filters out politics, sports, and low-quality noise. surfaces btc/eth markets with real liquidity and tight spreads.

## how it works

two parts:

- **`polymarket_bot.py`**: hits the polymarket gamma api every 15 seconds, scores each market, writes results to `signals.json`
- **the dashboard**: reads from that file and renders a live heatmap + signal feed with direct links to trade

## scoring

every market gets a tradability score from 0–100 based on:

| factor | weight |
|---|---|
| liquidity depth | 35% |
| daily volume | 35% |
| bid-ask spread | 30% |

btc and eth markets get a 1.5x multiplier. anything below 70 gets buried.

## features

- crypto-only, politics and sports are hardcoded out
- momentum flags for markets that moved fast in the last hour
- simulation mode to see entries without real money
- ui auto-refreshes every 5 seconds

## getting started

requires python 3.8+

**easy way:**
```bash
chmod +x run.sh
./run.sh
```

sets up a venv, installs deps, starts the bot, and serves the dashboard at `localhost:8080`.

**manual:**
```bash
pip install requests
python3 polymarket_bot.py
```
```bash
# new terminal
python3 -m http.server 8080
```
