import pandas as pd
import ta

from config.config import (
    BOLLINGER_PERIOD, BOLLINGER_STD_DEV,
    MACD_SHORT, MACD_LONG, MACD_SIGNAL,
    RSI_PERIOD,
    HIGHER_TF_RSI_PERIOD, HIGHER_TF_MACD_SHORT, HIGHER_TF_MACD_LONG, HIGHER_TF_MACD_SIGNAL,
    TREND_MA_PERIOD
)


def calculate_rsi(prices, period=RSI_PERIOD):
    return ta.momentum.RSIIndicator(pd.Series(prices), window=period).rsi().iloc[-1]


def calculate_macd(prices, short=MACD_SHORT, long=MACD_LONG, signal=MACD_SIGNAL):
    macd = ta.trend.MACD(pd.Series(prices), window_slow=long, window_fast=short, window_sign=signal)
    return macd.macd().iloc[-1], macd.macd_signal().iloc[-1]


def calculate_bollinger_bands(prices, period=BOLLINGER_PERIOD, std_dev=BOLLINGER_STD_DEV):
    prices = pd.Series(prices)
    rolling_mean = prices.rolling(window=period).mean()
    rolling_std = prices.rolling(window=period).std()
    upper_band = rolling_mean + (std_dev * rolling_std)
    lower_band = rolling_mean - (std_dev * rolling_std)
    return upper_band.iloc[-1], lower_band.iloc[-1]


def calculate_moving_average(prices, period=TREND_MA_PERIOD):
    series = pd.Series(prices)
    return series.rolling(window=period).mean().iloc[-1]


def calculate_higher_tf_indicators(prices):
    rsi = calculate_rsi(prices, period=HIGHER_TF_RSI_PERIOD)
    macd_val, signal_val = calculate_macd(prices, short=HIGHER_TF_MACD_SHORT, long=HIGHER_TF_MACD_LONG,
                                          signal=HIGHER_TF_MACD_SIGNAL)
    return rsi, macd_val, signal_val
