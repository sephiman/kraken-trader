from utils.utils import fetch_current_price, logger


def get_account_balance(api, pair):
    logger.info("Fetching account balance...")
    balance = api.query_private('Balance')['result']
    logger.info(f"Account balance fetched: {balance}")
    return {
        'base': float(balance.get(pair.split('/')[0], 0)),
        'quote': float(balance.get(pair.split('/')[1], 0))
    }

def place_buy_order(api, pair, quote_balance, amount):
    price = fetch_current_price(api, pair)
    logger.info(f"Current price for {pair}: {price}")
    max_volume = quote_balance / price
    if max_volume < 0.0001:
        logger.warning("Not enough funds to buy BTC")
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
        logger.warning("Not enough BTC to sell")
        return
    order = api.query_private('AddOrder', {
        'pair': pair.replace('/', ''),
        'type': 'sell',
        'ordertype': 'market',
        'volume': base_balance
    })
    logger.info(f"Sell order placed: {order}")

def execute_trade(action, api, pair, amount):
    logger.info(f"Executing {action.upper()} trade...")
    balance = get_account_balance(api, pair)
    if action == "buy":
        place_buy_order(api, pair, balance['quote'], amount)
    elif action == "sell":
        place_sell_order(api, pair, balance['base'])