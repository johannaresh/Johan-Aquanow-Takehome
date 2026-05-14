from datetime import datetime


class KPIComputer:
    def compute(self, coins):
        coins = [c for c in coins if c["price_change_percentage_24h"] is not None and c["market_cap"] is not None]

        sorted_coins = sorted(coins, key=lambda c: c["price_change_percentage_24h"])

        top_losers = sorted_coins[:3]
        top_gainers = sorted_coins[-3:]

        total_market_cap = sum(c["market_cap"] for c in coins)
        avg_market_cap = total_market_cap / len(coins)

        return {
            "timestamp": datetime.now().isoformat(),
            "top_gainers": [
                {
                    "name": c["name"],
                    "symbol": c["symbol"],
                    "change_24h": c["price_change_percentage_24h"],
                }
                for c in top_gainers
            ],
            "top_losers": [
                {
                    "name": c["name"],
                    "symbol": c["symbol"],
                    "change_24h": c["price_change_percentage_24h"],
                }
                for c in top_losers
            ],
            "average_market_cap_usd": avg_market_cap,
            "total_market_cap_usd": total_market_cap,
        }
