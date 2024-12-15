import time


def get_pl_from_kraken(api, days=1):
    since_timestamp = time.time() - (days * 86400)

    response = api.query_private('TradesHistory', {
        'start': since_timestamp
    })

    if response.get('error'):
        raise Exception(f"Error fetching trades: {response['error']}")

    trades = response['result']['trades']

    total_pl = 0.0
    for trade_id, trade_info in trades.items():
        t_type = trade_info['type']
        cost = float(trade_info['cost'])
        fee = float(trade_info['fee'])

        if t_type == 'buy':
            total_pl -= (cost + fee)
        elif t_type == 'sell':
            total_pl += (cost - fee)

    return total_pl
