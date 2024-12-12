from config.config import MIN_AMOUNT_TO_SELL
from utils.data_tracker import record_trade
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
    current_price = fetch_current_price(api, pair)
    base_asset = pair.split('/')[0]
    try:
        if action == "buy":
            order = place_buy_order(api, pair, balance['quote'], amount)
            base_bought = amount / current_price
            if order:
                usd_spent = amount
                message = (
                    f"Buy trade executed successfully for {pair}:\n"
                    f"- Amount: {usd_spent:.2f} USD\n"
                    f"- Bought: {base_bought:.2f} USD\n"
                    f"- Price: {current_price:.2f} USD\n"
                    f"- Order Details: {order}"
                )
            record_trade("buy", pair, amount, current_price, base_bought, amount)
        elif action == "sell":
            if balance['base'] < MIN_AMOUNT_TO_SELL:
                message = (
                    f"Attempted to sell {pair} at price {current_price:.2f}, "
                    f"but no balance available (Current base balance: {balance['base']:.8f})."
                )
                logger.warning(message)
                return
            order = place_sell_order(api, pair, balance['base'])
            base_sold = balance['base']
            usd_value = base_sold * current_price
            if order:
                message = (
                    f"Sell trade executed successfully for {pair}:\n"
                    f"- Amount Sold: {base_sold:.8f} {base_asset} (~{usd_value:.2f} USD)\n"
                    f"- Price: {current_price:.2f} USD\n"
                    f"- Order Details: {order}"
                )
            record_trade("sell", pair, usd_value, current_price, base_sold, usd_value)
        else:
            raise ValueError(f"Invalid trade action: {action}")

        if order:
            logger.info(message)
            send_telegram_message(message)
        else:
            raise Exception("Order placement failed")

    except Exception as e:
        message = f"{action.capitalize()} trade failed for {pair} with current price {current_price:.2f}: {e}"
        logger.error(message)
        send_telegram_message(message)
