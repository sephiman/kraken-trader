import os

KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

PAIR = os.getenv("PAIR")
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 10))
NEW_BUY_THRESHOLD = float(os.getenv("NEW_BUY_THRESHOLD", 0.05))

# RSI (Relative Strength Index) Configuration
RSI_PERIOD = 7  # Number of periods used for calculating RSI
RSI_OVERBOUGHT = 60  # RSI value above which the asset is considered overbought (sell signal)
RSI_OVERSOLD = 40  # RSI value below which the asset is considered oversold (buy signal)

# MACD (Moving Average Convergence Divergence) Configuration
MACD_SHORT = 8  # Short-term EMA (Exponential Moving Average) period for MACD
MACD_LONG = 21  # Long-term EMA period for MACD
MACD_SIGNAL = 5  # Signal line EMA period used to generate buy/sell crossovers

# Bollinger Bands settings
BOLLINGER_PERIOD = 14  # The lookback period for calculating the moving average.
# Example: A period of 14 means the Bollinger Bands are calculated using the last 14 price candles.

BOLLINGER_STD_DEV = 1.5  # The number of standard deviations added/subtracted from the moving average to calculate the upper and lower bands.
# Example: A value of 1.5 means the bands are 1.5 standard deviations away from the moving average,
# providing a narrower or wider range for detecting price volatility.


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LOG_FILE = os.getenv("LOG_FILE", "./logs/trading_bot.log")
