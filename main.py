import time
import krakenex
from utils.indicators import calculate_rsi, calculate_macd
from utils.logger import setup_logger
from config import KRAKEN_API_KEY, KRAKEN_API_SECRET, PAIR, TRADE_AMOUNT, RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD, MACD_SHORT, MACD_LONG, MACD_SIGNAL

api = krakenex.API(KRAKEN_API_KEY, KRAKEN_API_SECRET)
logger = setup_logger()

def fetch_ohlc(pair, interval):
    """Fetch OHLC data from Kraken."""
    try:
        logger.info(f"Fetching OHLC data for {pair} with interval {interval}")
        response = api.query_public('OHLC', {'pair': pair.replace('/', ''), 'interval': interval})
        data = response['result'][list(response['result'].keys())[0]]
        prices = [float(item[4]) for item in data]  # Closing prices
        logger.info(f"Successfully fetched {len(prices)} OHLC data points")
        return prices
    except Exception as e:
        logger.error(f"Failed to fetch OHLC data: {e}")
        return []

def execute_trade(action, pair, amount):
    """Execute a trade on Kraken."""
    try:
        logger.info(f"Attempting to place a {action.upper()} order for {amount} of {pair}")
        if action == "buy":
            order = api.query_private('AddOrder', {'pair': pair.replace('/', ''), 'type': 'buy', 'ordertype': 'market', 'volume': amount})
        elif action == "sell":
            order = api.query_private('AddOrder', {'pair': pair.replace('/', ''), 'type': 'sell', 'ordertype': 'market', 'volume': amount})
        logger.info(f"{action.capitalize()} order placed successfully: {order}")
    except Exception as e:
        logger.error(f"Trade execution failed: {e}")

def scalping_bot():
    """Main scalping bot logic."""
    while True:
        logger.info("Starting a new iteration of the scalping bot...")
        prices = fetch_ohlc(PAIR, interval=1)  # Fetch 1-minute data
        if not prices:
            logger.warning("No prices fetched, sleeping for 60 seconds...")
            time.sleep(60)
            continue

        logger.info(f"Calculating RSI and MACD indicators for {PAIR}")
        rsi = calculate_rsi(prices, RSI_PERIOD)
        macd, signal_line = calculate_macd(prices, MACD_SHORT, MACD_LONG, MACD_SIGNAL)

        if len(rsi) < RSI_PERIOD or len(macd) < MACD_SIGNAL:
            logger.warning("Insufficient data for indicators, sleeping for 60 seconds...")
            time.sleep(60)
            continue

        # Get the latest RSI and MACD values
        current_rsi = rsi.iloc[-1]
        current_macd = macd.iloc[-1]
        current_signal = signal_line.iloc[-1]

        logger.info(f"Latest indicators: RSI={current_rsi:.2f}, MACD={current_macd:.2f}, Signal Line={current_signal:.2f}")

        # Decision-making
        if current_rsi < RSI_OVERSOLD and current_macd > current_signal:
            logger.info("Buy signal detected: RSI indicates oversold and MACD shows bullish crossover")
            execute_trade("buy", PAIR, TRADE_AMOUNT)
        elif current_rsi > RSI_OVERBOUGHT and current_macd < current_signal:
            logger.info("Sell signal detected: RSI indicates overbought and MACD shows bearish crossover")
            execute_trade("sell", PAIR, TRADE_AMOUNT)
        else:
            logger.info("No trade signal detected, sleeping for 60 seconds...")

        time.sleep(60)

if __name__ == "__main__":
    logger.info("Starting Kraken Trading Bot")
    try:
        scalping_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
