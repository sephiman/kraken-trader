import time
from datetime import datetime, UTC

from config.config import (
    PAIR, TRADE_AMOUNT, RSI_OVERBOUGHT, RSI_OVERSOLD, NEW_BUY_THRESHOLD,
    TREND_FILTER_ENABLED, TREND_MA_PERIOD,
    HIGHER_TF_CONFIRMATION_ENABLED, HIGHER_TF_INTERVAL,
    HIGHER_TF_RSI_OVERBOUGHT, HIGHER_TF_RSI_OVERSOLD, INTERVAL_MINUTE
)
from core.account import execute_trade, get_account_balance
from core.indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger_bands,
    calculate_moving_average, calculate_higher_tf_indicators
)
from utils.kraken_pl import get_pl_from_kraken
from utils.logger import logger
from utils.telegram import send_telegram_message
from utils.utils import fetch_ohlc


def check_trend_filter(prices, current_price):
    ma = calculate_moving_average(prices, period=TREND_MA_PERIOD)
    return current_price > ma, current_price < ma


def check_higher_tf_confirmation(api, pair):
    if not HIGHER_TF_CONFIRMATION_ENABLED:
        return True, True
    higher_tf_prices = fetch_ohlc(api, pair, interval=HIGHER_TF_INTERVAL)
    if not higher_tf_prices or len(higher_tf_prices) < 30:
        return True, True

    htf_rsi, htf_macd, htf_signal = calculate_higher_tf_indicators(higher_tf_prices)

    buy_confirm = (htf_rsi < HIGHER_TF_RSI_OVERSOLD and htf_macd > htf_signal)
    sell_confirm = (htf_rsi > HIGHER_TF_RSI_OVERBOUGHT and htf_macd < htf_signal)

    return buy_confirm, sell_confirm


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
    daily_summary_sent = False
    last_buy_price = None
    while True:
        try:
            logger.info("Starting a new iteration ...")
            prices = fetch_ohlc(api, PAIR, interval=INTERVAL_MINUTE)
            if not prices:
                logger.warning("No prices fetched, sleeping for 60 seconds...")
                time.sleep(60)
                continue

            current_price = prices[-1]
            rsi = calculate_rsi(prices)
            macd, signal = calculate_macd(prices)
            upper_band, lower_band = calculate_bollinger_bands(prices)
            drop_percentage = ((last_buy_price - current_price) / last_buy_price) * 100 if last_buy_price else None

            drop_percentage_str = f"{drop_percentage:.2f}%" if drop_percentage is not None else "N/A"

            buy_confirm, sell_confirm = check_higher_tf_confirmation(api, PAIR)

            buy_trend_ok, sell_trend_ok = True, True
            if TREND_FILTER_ENABLED:
                buy_trend_ok, sell_trend_ok = check_trend_filter(prices, current_price)

            log_message = (
                f"RSI: {rsi:.2f}, MACD: {macd:.2f}, Signal: {signal:.2f}, "
                f"Upper Band: {upper_band:.2f}, Lower Band: {lower_band:.2f}, "
                f"Drop Percentage: {drop_percentage_str}, "
                f"Current Price {PAIR}: {current_price:.2f}, "
                f"Buy Trend OK: {buy_trend_ok}, Sell Trend OK: {sell_trend_ok}"
            )
            logger.info(log_message)

            if should_buy(rsi, macd, signal, current_price, lower_band,
                          drop_percentage) and buy_confirm and buy_trend_ok:
                message = (
                    f"Buy signal detected for {PAIR}:\n"
                    f"- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Signal: {signal:.2f}\n"
                    f"- Price: {current_price:.2f}\n(Higher TF Confirm: {buy_confirm}, Trend OK: {buy_trend_ok})"
                )
                logger.info(message)
                execute_trade("buy", api, PAIR, TRADE_AMOUNT)
                last_buy_price = current_price
            elif should_sell(rsi, macd, signal, current_price, upper_band) and sell_confirm and sell_trend_ok:
                message = (
                    f"Sell signal detected for {PAIR}:\n"
                    f"- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Signal: {signal:.2f}\n"
                    f"- Price: {current_price:.2f}\n(Higher TF Confirm: {sell_confirm}, Trend OK: {sell_trend_ok})"
                )
                logger.info(message)
                execute_trade("sell", api, PAIR, TRADE_AMOUNT)
                last_buy_price = None
            else:
                logger.info("No trade signal detected or not confirmed by trend/higher TF, sleeping for 60 seconds...")

            daily_summary_sent = send_summary(api, daily_summary_sent)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            send_telegram_message(f"Error in bot execution: {e}")

        time.sleep(INTERVAL_MINUTE * 60)


def send_summary(api, daily_summary_sent):
    current_hour_utc = datetime.now(tz=UTC).hour
    if current_hour_utc == 0 and not daily_summary_sent:
        balance = get_account_balance(api, PAIR)

        last_24h_pl = get_pl_from_kraken(api, days=1)
        last_7d_pl = get_pl_from_kraken(api, days=7)
        last_30d_pl = get_pl_from_kraken(api, days=30)

        summary_message = (
            f"Daily Summary:\n"
            f"Current balance: {balance['base']} {PAIR} and {balance['quote']} USD\n"
            f"Last 24h P/L: {last_24h_pl:.2f} USD\n"
            f"Last 7d P/L: {last_7d_pl:.2f} USD\n"
            f"Last 30d P/L: {last_30d_pl:.2f} USD"
        )
        send_telegram_message(summary_message)
        return True
    elif current_hour_utc != 0:
        return False
    return daily_summary_sent
