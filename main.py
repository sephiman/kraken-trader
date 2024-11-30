import os
import krakenex
from core.bot import scalping_bot
from utils.logger import logger

KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

if __name__ == "__main__":
    try:
        # Initialize Kraken API client with credentials
        api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)
        logger.info("Starting Kraken Trading Bot")
        scalping_bot(api)  # Pass the `api` object to the bot
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
