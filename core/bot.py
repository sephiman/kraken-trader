import time

from config.config import PAIR, TRADE_AMOUNT, RSI_OVERBOUGHT, RSI_OVERSOLD
from core.account import execute_trade
from core.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands
from utils.logger import logger
from utils.telegram import send_telegram_message
from utils.utils import fetch_ohlc


def should_buy(rsi, macd, signal, price, lower_band):
    return rsi < RSI_OVERSOLD and macd > signal and price <= lower_band


def should_sell(rsi, macd, signal, price, upper_band):
    return rsi > RSI_OVERBOUGHT and macd < signal and price >= upper_band


def bot(api):
    while True:
        logger.info("Starting a new iteration of the scalping bot...")
        prices = fetch_ohlc(api, PAIR, interval=1)
        if not prices:
            logger.warning("No prices fetched, sleeping for 60 seconds...")
            time.sleep(60)
            continue

        current_price = prices[-1]
        rsi = calculate_rsi(prices)
        macd, signal = calculate_macd(prices)
        upper_band, lower_band = calculate_bollinger_bands(prices)

        logger.info(
            f"RSI: {rsi:.2f}, MACD: {macd:.2f}, Signal: {signal:.2f}, Upper Band: {upper_band:.2f}, Lower Band: {lower_band:.2f}")

        if should_buy(rsi, macd, signal, current_price, lower_band):
            message = f"Buy signal detected for {PAIR}:\n- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Signal: {signal:.2f}\n- Price: {current_price:.2f}"
            logger.info(message)
            send_telegram_message(message)
            execute_trade("buy", api, PAIR, TRADE_AMOUNT)
        elif should_sell(rsi, macd, signal, current_price, upper_band):
            message = f"Sell signal detected for {PAIR}:\n- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Signal: {signal:.2f}\n- Price: {current_price:.2f}"
            logger.info(message)
            send_telegram_message(message)
            execute_trade("sell", api, PAIR, TRADE_AMOUNT)
        else:
            logger.info("No trade signal detected, sleeping for 60 seconds...")

        time.sleep(60)
