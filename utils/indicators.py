import pandas as pd
import ta

def calculate_rsi(prices, period):
    """Calculate the RSI for a given price series."""
    return ta.momentum.RSIIndicator(pd.Series(prices), window=period).rsi()

def calculate_macd(prices, short_window, long_window, signal_window):
    """Calculate MACD and Signal Line."""
    macd = ta.trend.MACD(pd.Series(prices),
                         window_slow=long_window,
                         window_fast=short_window,
                         window_sign=signal_window)
    return macd.macd(), macd.macd_signal()
