import os

EXCHANGE = os.getenv("EXCHANGE").upper()

API_KEY = os.getenv("API_KEY")
SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("API_PASSPHRASE")

PAIR = os.getenv("PAIR")
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 10))
NEW_BUY_THRESHOLD = float(os.getenv("NEW_BUY_THRESHOLD", 0.02))
MIN_AMOUNT_TO_SELL = float(os.getenv("MIN_AMOUNT", 0.000001))
INTERVAL_MINUTE = 5

# RSI (Relative Strength Index) Configuration
RSI_PERIOD = 14  # Number of periods used for calculating RSI
RSI_OVERBOUGHT = 58  # RSI value above which the asset is considered overbought (sell signal)
RSI_OVERSOLD = 52  # RSI value below which the asset is considered oversold (buy signal)

# MACD (Moving Average Convergence Divergence) Configuration
MACD_SHORT = 5  # Short-term EMA (Exponential Moving Average) period for MACD
MACD_LONG = 12  # Long-term EMA period for MACD
MACD_SIGNAL = 3  # Signal line EMA period used to generate buy/sell crossovers

# Bollinger Bands settings
BOLLINGER_PERIOD = 20  # The lookback period for calculating the moving average.
# Example: A period of 14 means the Bollinger Bands are calculated using the last 14 price candles.

BOLLINGER_STD_DEV = 1.2  # The number of standard deviations added/subtracted from the moving average to calculate the upper and lower bands.
# Example: A value of 1.5 means the bands are 1.5 standard deviations away from the moving average,
# providing a narrower or wider range for detecting price volatility.

# Confirmation signals
# Trend filter parameters
TREND_FILTER_ENABLED = False
TREND_MA_PERIOD = 10

# Higher timeframe confirmation
HIGHER_TF_CONFIRMATION_ENABLED = False
HIGHER_TF_INTERVAL = 15  # 5-minute bars
HIGHER_TF_RSI_PERIOD = 14
HIGHER_TF_RSI_OVERBOUGHT = 65
HIGHER_TF_RSI_OVERSOLD = 40
HIGHER_TF_MACD_SHORT = 12
HIGHER_TF_MACD_LONG = 26
HIGHER_TF_MACD_SIGNAL = 9


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LOG_FILE = os.getenv("LOG_FILE", "./logs/trading_bot.log")
