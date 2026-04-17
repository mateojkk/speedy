import requests
import json
import time
from datetime import datetime

class SpeedyBot:
    def __init__(self):
        self.gamma_url = "https://gamma-api.polymarket.com/events"
        self.params = {
            "limit": 300, # fetch top 300 to bypass sports-heavy default sorting
            "active": "true",
            "closed": "false"
        }
        
    def fetch_data(self):
        try:
            response = requests.get(self.gamma_url, params=self.params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

    def calculate_score(self, liquidity, vol24, spread, hr_change, tags):
        # Base constraints to filter garbage
        if liquidity < 2000 or vol24 < 1000:
            return 0
        
        # We max out liquidity score at $100k, vol at $50k, spread max 10 cents
        lq_score = min(liquidity / 100000, 1.0) * 35
        vol_score = min(vol24 / 50000, 1.0) * 35
        sp_score = min(spread / 0.10, 1.0) * 30
        
        base_score = lq_score + vol_score + sp_score
        
        # Sector Filter - The user wants BTC and ETH only.
        multiplier = 1.0
        
        # Priority Tags
        boost_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'blockchain']
        # Penalty Tags - Extensive list to kill anything remotely political or sporty
        penalty_keywords = [
            'politics', 'elections', 'election', 'donald trump', 'kamala harris', 
            'starmer', 'uk', 'government', 'senate', 'biden', 'white house',
            'sports', 'nba', 'soccer', 'nfl', 'hockey', 'mlb', 'champions league', 
            'premier league', 'basketball', 'football', 'baseball', 'ufc', 'tennis'
        ]
        
        tag_str = " ".join([t.lower() for t in tags])
        
        # 1. Hard fail on penalties
        if any(kp in tag_str for kp in penalty_keywords):
            return 0
            
        # 2. Require at least one crypto keyword or it's not a signal
        is_crypto = any(kb in tag_str for kb in boost_keywords)
        if not is_crypto:
            return 0 
            
        # 3. Apply Boost for explicitly requested BTC/ETH
        multiplier += 1.5 
            
        final_score = base_score * multiplier
        
        # Momentum multiplier
        if abs(hr_change) >= 0.05:
            final_score = final_score * 1.25
        elif abs(hr_change) >= 0.02:
            final_score = final_score * 1.1

        return round(min(100, final_score), 1)

    def analyze_system(self, events):
        signals = []
        sectors = {}
        
        priority_order = ['Crypto', 'Bitcoin', 'Ethereum']
        penalty_keywords = [
            'politics', 'elections', 'election', 'donald trump', 'kamala harris', 
            'starmer', 'uk', 'government', 'senate', 'biden', 'white house',
            'sports', 'nba', 'soccer', 'nfl', 'hockey', 'mlb', 'champions league', 
            'premier league', 'basketball', 'football', 'baseball', 'ufc', 'tennis'
        ]

        for event in events:
            evt_tags = [t.get('label', 'Uncategorized') for t in event.get('tags', [])]
            evt_slug = event.get('slug', '')
            markets = event.get('markets', [])
            
            # Skip entire event if any tag is penalized
            tag_str = " ".join([t.lower() for t in evt_tags])
            if any(kp in tag_str for kp in penalty_keywords):
                continue
            
            for market in markets:
                market_id = market.get('id')
                question = market.get('question')
                liquidity = float(market.get('liquidity') or 0)
                vol24 = float(market.get('volume24hr') or 0)
                best_bid = float(market.get('bestBid') or 0)
                best_ask = float(market.get('bestAsk') or 0)
                spread = float(market.get('spread') or 0)
                hr_change = float(market.get('oneHourPriceChange') or 0)
                
                # Update sector aggregates (only for non-penalized)
                for tag in evt_tags:
                    if tag not in sectors:
                        sectors[tag] = {'vol': 0, 'liquidity': 0, 'momentum': 0, 'count': 0}
                    sectors[tag]['vol'] += vol24
                    sectors[tag]['liquidity'] += liquidity
                    sectors[tag]['momentum'] += hr_change
                    sectors[tag]['count'] += 1

                score = self.calculate_score(liquidity, vol24, spread, hr_change, evt_tags)
                if score < 1:
                    continue

                # EV Calculation
                max_edge_val = spread * min(liquidity, vol24)
                
                signal_type = "CRYPTO_ALPHA"
                if abs(hr_change) >= 0.05: signal_type = "MOMENTUM_PLAY"
                
                signals.append({
                    "id": market_id,
                    "slug": evt_slug,
                    "timestamp": datetime.now().isoformat()[-15:-7],
                    "type": signal_type,
                    "question": question[:60] + "..." if len(question) > 60 else question,
                    "score": score,
                    "metrics": {
                        "liquidity": round(liquidity),
                        "vol24": round(vol24),
                        "spread": round(spread, 3),
                        "hr_change": round(hr_change, 3),
                        "best_bid": best_bid,
                        "best_ask": best_ask,
                        "est_ev_cap": round(max_edge_val, 2)
                    },
                    "tags": evt_tags[:2]
                })

        # Process Sectors heatmap - Filter out noise tags
        ignore_tags = ['Hide From New', 'Week 17', 'Uncategorized', 'Featured', 'Starmer', 'uk', 'Politics']
        heatmap_data = []
        for tag, data in sectors.items():
            if tag in ignore_tags: continue
            # Only show if explicitly crypto-related
            if not any(kb in tag.lower() for kb in ['crypto', 'bitcoin', 'btc', 'ethereum', 'eth', 'blockchain']):
                continue
            if data['count'] > 0 and data['vol'] > 100:
                heatmap_data.append({
                    "sector": tag,
                    "vol": round(data['vol']),
                    "lq": round(data['liquidity']),
                    "avg_mom": round((data['momentum'] / data['count']) * 100, 2)
                })
        
        def heatmap_sort(x):
            try:
                p_score = priority_order.index(x['sector'])
            except ValueError:
                p_score = 99
            return (p_score, -x['vol'])

        heatmap_data = sorted(heatmap_data, key=heatmap_sort)[:10]
        signals = sorted(signals, key=lambda x: x['score'], reverse=True)[:25]

        return {
            "last_updated": datetime.now().isoformat(),
            "markets_scanned": sum(len(e.get('markets', [])) for e in events),
            "heatmap": heatmap_data,
            "signals": signals
        }

    def run_loop(self):
        print("Starting Speedy Daemon (CRYPTO MODE)...")
        while True:
            events = self.fetch_data()
            if events:
                system_state = self.analyze_system(events)
                try:
                    with open("signals.json", "w") as f:
                        json.dump(system_state, f, indent=2)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Pulse Sync: {len(system_state['signals'])} crypto signals generated.")
                except Exception as e:
                    print(f"Failed to write JSON: {e}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetch failed, retrying...")
            
            time.sleep(15)

if __name__ == "__main__":
    bot = SpeedyBot()
    bot.run_loop()
