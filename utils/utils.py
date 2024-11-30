from utils.logger import logger


def fetch_ohlc(api, pair, interval=1):
    logger.info(f"Fetching OHLC data for {pair} with interval {interval}")
    response = api.query_public('OHLC', {'pair': pair.replace('/', ''), 'interval': interval})
    data = response['result'][list(response['result'].keys())[0]]
    prices = [float(item[4]) for item in data]
    logger.info(f"Fetched {len(prices)} OHLC data points for {pair}")
    return prices

def fetch_current_price(api, pair):
    logger.info(f"Fetching current price for {pair}")
    ticker = api.query_public('Ticker', {'pair': pair.replace('/', '')})
    return float(ticker['result'][list(ticker['result'].keys())[0]]['c'][0])
