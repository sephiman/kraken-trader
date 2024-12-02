from utils.utils import fetch_current_price, logger


def get_account_balance(api, pair):
    logger.debug("Fetching account balance...")
    balance = api.query_private('Balance')['result']
    logger.debug(f"Account balance fetched: {balance}")

    asset_map = {
        "BTC": "XXBT",
        "ETH": "XETH",
        "USD": "ZUSD",
        "EUR": "ZEUR"
    }

    base_asset, quote_asset = pair.split('/')  # E.g., BTC/USD -> base: BTC, quote: USD
    base_balance = float(balance.get(asset_map.get(base_asset, base_asset), 0))
    quote_balance = float(balance.get(asset_map.get(quote_asset, quote_asset), 0))

    logger.info(f"Base balance ({base_asset}): {base_balance:.8f}, Quote balance ({quote_asset}): {quote_balance:.2f}")
    return {'base': base_balance, 'quote': quote_balance}


def place_buy_order(api, pair, quote_balance, amount):
    price = fetch_current_price(api, pair)
    logger.debug(f"Current price for {pair}: {price}")
    max_volume = quote_balance / price
    if max_volume < 0.0001:
        logger.warning(f"Not enough funds to buy {pair}")
        return
    volume = min(amount, max_volume)
    order = api.query_private('AddOrder', {
        'pair': pair.replace('/', ''),
        'type': 'buy',
        'ordertype': 'market',
        'volume': volume
    })
    logger.info(f"Buy order placed: {order}")


def place_sell_order(api, pair, base_balance):
    if base_balance < 0.0001:
        logger.warning(f"Not enough {pair} to sell")
        return
    order = api.query_private('AddOrder', {
        'pair': pair.replace('/', ''),
        'type': 'sell',
        'ordertype': 'market',
        'volume': base_balance
    })
    logger.info(f"Sell order placed: {order}")


def execute_trade(action, api, pair, amount):
    logger.debug(f"Executing {action.upper()} trade...")
    balance = get_account_balance(api, pair)
    if action == "buy":
        place_buy_order(api, pair, balance['quote'], amount)
    elif action == "sell":
        place_sell_order(api, pair, balance['base'])
