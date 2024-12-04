import time

from config.config import PAIR, TRADE_AMOUNT, RSI_OVERBOUGHT, RSI_OVERSOLD, NEW_BUY_THRESHOLD
from core.account import execute_trade
from core.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands
from utils.logger import logger
from utils.telegram import send_telegram_message
from utils.utils import fetch_ohlc


def should_buy(rsi, macd, signal, price, lower_band, drop_percentage):
    if drop_percentage is None:
        logger.debug("No last buy price recorded; skipping drop percentage check.")
        significant_drop = True
    else:
        significant_drop = drop_percentage >= NEW_BUY_THRESHOLD
        logger.debug(
            f"Drop Percentage: {drop_percentage:.2f}% (Threshold: {NEW_BUY_THRESHOLD}%) - Significant: {significant_drop}")

    return rsi < RSI_OVERSOLD and macd > signal and price <= lower_band and significant_drop


def should_sell(rsi, macd, signal, price, upper_band):
    return rsi > RSI_OVERBOUGHT and macd < signal and price >= upper_band


def bot(api):
    last_buy_price = None
    while True:
        try:
            logger.info("Starting a new iteration ...")
            prices = fetch_ohlc(api, PAIR, interval=1)
            if not prices:
                logger.warning("No prices fetched, sleeping for 60 seconds...")
                time.sleep(60)
                continue

            current_price = prices[-1]
            rsi = calculate_rsi(prices)
            macd, signal = calculate_macd(prices)
            upper_band, lower_band = calculate_bollinger_bands(prices)
            drop_percentage = ((last_buy_price - current_price) / last_buy_price) * 100 if last_buy_price else None

            logger.info(
                f"RSI: {rsi:.2f}, MACD: {macd:.2f}, Signal: {signal:.2f}, "
                f"Upper Band: {upper_band:.2f}, Lower Band: {lower_band:.2f}, "
                f"Drop Percentage: {drop_percentage:.2f}%" if drop_percentage is not None else "Drop Percentage: N/A"
            )

            if should_buy(rsi, macd, signal, current_price, lower_band, drop_percentage):
                message = f"Buy signal detected for {PAIR}:\n- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Signal: {signal:.2f}\n- Price: {current_price:.2f}"
                logger.info(message)
                execute_trade("buy", api, PAIR, TRADE_AMOUNT)
                last_buy_price = current_price
            elif should_sell(rsi, macd, signal, current_price, upper_band):
                message = f"Sell signal detected for {PAIR}:\n- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Signal: {signal:.2f}\n- Price: {current_price:.2f}"
                logger.info(message)
                execute_trade("sell", api, PAIR, TRADE_AMOUNT)
                last_buy_price = None
            else:
                logger.info("No trade signal detected, sleeping for 60 seconds...")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            send_telegram_message(f"Error in bot execution: {e}")

        time.sleep(60)
