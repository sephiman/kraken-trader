import pandas as pd
import ta

from config.config import BOLLINGER_PERIOD, BOLLINGER_STD_DEV


def calculate_rsi(prices, period=14):
    return ta.momentum.RSIIndicator(pd.Series(prices), window=period).rsi().iloc[-1]


def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    macd = ta.trend.MACD(pd.Series(prices), window_slow=long_window, window_fast=short_window,
                         window_sign=signal_window)
    return macd.macd().iloc[-1], macd.macd_signal().iloc[-1]


def calculate_bollinger_bands(prices, period=BOLLINGER_PERIOD, std_dev=BOLLINGER_STD_DEV):
    prices = pd.Series(prices)
    rolling_mean = prices.rolling(window=period).mean()
    rolling_std = prices.rolling(window=period).std()
    upper_band = rolling_mean + (std_dev * rolling_std)
    lower_band = rolling_mean - (std_dev * rolling_std)
    return upper_band.iloc[-1], lower_band.iloc[-1]
