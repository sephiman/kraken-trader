from utils.telegram import send_telegram_message
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
    trade_volume = amount / price
    max_volume = quote_balance / price
    volume = min(trade_volume, max_volume)

    order = api.query_private('AddOrder', {
        'pair': pair.replace('/', ''),
        'type': 'buy',
        'ordertype': 'market',
        'volume': volume
    })
    logger.info(f"Buy order placed: {order}")
    return order


def place_sell_order(api, pair, base_balance):
    if base_balance < 0.0001:
        message = f"Not enough {pair} to sell"
        logger.warning(message)
        return None
    order = api.query_private('AddOrder', {
        'pair': pair.replace('/', ''),
        'type': 'sell',
        'ordertype': 'market',
        'volume': base_balance
    })
    logger.info(f"Sell order placed: {order}")
    return order


def execute_trade(action, api, pair, amount):
    logger.debug(f"Executing {action.upper()} trade...")
    balance = get_account_balance(api, pair)

    try:
        if action == "buy":
            order = place_buy_order(api, pair, balance['quote'], amount)
        elif action == "sell":
            order = place_sell_order(api, pair, balance['base'])
        else:
            raise ValueError(f"Invalid trade action: {action}")

        if order:
            message = f"{action.capitalize()} trade executed successfully for {pair}:\n" \
                      f"- Amount: {amount}\n" \
                      f"- Order Details: {order}"
            logger.info(message)
            send_telegram_message(message)
        else:
            raise Exception("Order placement failed")

    except Exception as e:
        message = f"{action.capitalize()} trade failed for {pair}: {e}"
        logger.error(message)
        send_telegram_message(message)
