import krakenex

from config.config import KRAKEN_API_KEY, KRAKEN_API_SECRET
from core.bot import bot
from utils.logger import logger

if __name__ == "__main__":
    try:
        api = krakenex.API(key=KRAKEN_API_KEY, secret=KRAKEN_API_SECRET)
        logger.info("Starting Kraken Trading Bot")
        bot(api)  # Pass the `api` object to the bot
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
