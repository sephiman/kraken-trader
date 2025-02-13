from utils.logger import logger


def fetch_ohlc(api, pair, interval=1):
    logger.debug(f"Fetching OHLC data for {pair} with interval {interval}")
    return api.fetch_ohlc(pair, interval)

def fetch_current_price(api, pair):
    logger.debug(f"Fetching current price for {pair}")
    return api.fetch_current_price(pair)
