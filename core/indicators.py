import pandas as pd
import ta

from config.config import BOLLINGER_PERIOD, BOLLINGER_STD_DEV, MACD_SHORT, MACD_LONG, MACD_SIGNAL, RSI_PERIOD


def calculate_rsi(prices):
    return ta.momentum.RSIIndicator(pd.Series(prices), window=RSI_PERIOD).rsi().iloc[-1]


def calculate_macd(prices):
    macd = ta.trend.MACD(pd.Series(prices), window_slow=MACD_LONG, window_fast=MACD_SHORT,
                         window_sign=MACD_SIGNAL)
    return macd.macd().iloc[-1], macd.macd_signal().iloc[-1]


def calculate_bollinger_bands(prices, period=BOLLINGER_PERIOD, std_dev=BOLLINGER_STD_DEV):
    prices = pd.Series(prices)
    rolling_mean = prices.rolling(window=period).mean()
    rolling_std = prices.rolling(window=period).std()
    upper_band = rolling_mean + (std_dev * rolling_std)
    lower_band = rolling_mean - (std_dev * rolling_std)
    return upper_band.iloc[-1], lower_band.iloc[-1]
