from config.config import API_KEY, SECRET, EXCHANGE, PASSPHRASE
from core.bot import bot
from utils.exchange_api import KrakenAPIAdapter, BitgetAPIAdapter
from utils.logger import logger

if __name__ == "__main__":
    try:
        if EXCHANGE == "KRAKEN":
            api = KrakenAPIAdapter(api_key=API_KEY, api_secret=SECRET)
        elif EXCHANGE == "BITGET":
            api = BitgetAPIAdapter(api_key=API_KEY, api_secret=SECRET, passphrase=PASSPHRASE)
        else:
            raise ValueError(f"Unsupported exchange: {EXCHANGE}")

        logger.info(f"Starting Trading Bot on {EXCHANGE}")
        bot(api)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
