import json
import os
from datetime import datetime, timedelta, UTC
from typing import Dict, Any

DATA_FILE = os.getenv("TRADE_HISTORY", "./logs/trade_history.json")

def record_trade(action, pair, amount, price, base_volume, usd_spent_or_gained):
    data = load_data()
    trade_entry = {
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "action": action,
        "pair": pair,
        "amount": amount,
        "price": price,
        "base_volume": base_volume,
        "usd_value": usd_spent_or_gained
    }
    data["trades"].append(trade_entry)
    save_data(data)


def record_balance(balance):
    data = load_data()
    balance_entry = {
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "balance": balance  # {"base": x, "quote": y}
    }
    data["balances"].append(balance_entry)
    save_data(data)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"trades": [], "balances": []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data: Dict[str, Any]):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def get_summary(days=1):
    data = load_data()
    cutoff = datetime.now(tz=UTC) - timedelta(days=days)
    trades_in_period = [t for t in data["trades"] if datetime.fromisoformat(t["timestamp"]) > cutoff]

    realized_pl = sum(t["usd_value"] for t in trades_in_period if t["action"] == "sell") - \
                  sum(t["usd_value"] for t in trades_in_period if t["action"] == "buy")

    return realized_pl
