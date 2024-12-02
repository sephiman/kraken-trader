import os

KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

# Trading pair
PAIR = os.getenv("PAIR")
TRADE_AMOUNT = os.getenv("TRADE_AMOUNT")
RSI_PERIOD = 14
RSI_OVERBOUGHT = 60
RSI_OVERSOLD = 40
MACD_SHORT = 12
MACD_LONG = 26
MACD_SIGNAL = 9

LOG_FILE = os.getenv("LOG_FILE", "./logs/trading_bot.log")
