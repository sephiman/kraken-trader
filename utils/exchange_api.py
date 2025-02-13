import base64
import hashlib
import hmac
import json
import time

import krakenex
import requests
from urllib.parse import urlencode

class KrakenAPIAdapter:
    def __init__(self, api_key, api_secret):
        self.api = krakenex.API(key=api_key, secret=api_secret)

    def fetch_current_price(self, pair):
        # Kraken expects the pair without a slash.
        response = self.api.query_public('Ticker', {'pair': pair.replace('/', '')})
        result = response.get('result', {})
        pair_key = list(result.keys())[0]
        return float(result[pair_key]['c'][0])

    def fetch_ohlc(self, pair, interval):
        response = self.api.query_public('OHLC', {'pair': pair.replace('/', ''), 'interval': interval})
        result = response.get('result', {})
        pair_key = list(result.keys())[0]
        data = result[pair_key]
        # Use the closing price (item[4] in each candle)
        prices = [float(item[4]) for item in data]
        return prices

    def get_balance(self, pair):
        response = self.api.query_private('Balance')
        balance_data = response.get('result', {})
        asset_map = {
            "BTC": "XXBT",
            "ETH": "XETH",
            "USD": "ZUSD",
            "EUR": "ZEUR"
        }
        base_asset, quote_asset = pair.split('/')
        base_balance = float(balance_data.get(asset_map.get(base_asset, base_asset), 0))
        quote_balance = float(balance_data.get(asset_map.get(quote_asset, quote_asset), 0))
        return {'base': base_balance, 'quote': quote_balance}

    def place_order(self, order_type, pair, volume):
        order_params = {
            'pair': pair.replace('/', ''),
            'type': order_type,
            'ordertype': 'market',
            'volume': volume
        }
        response = self.api.query_private('AddOrder', order_params)
        return response


class BitgetAPIAdapter:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = "https://api.bitget.com/api/v2/mix"

    def _get_timestamp(self):
        return str(int(time.time() * 1000))

    def _generate_sign(self, timestamp, method, request_path, body=""):
        """
        Generate the ACCESS-SIGN using HMAC SHA256 and base64 encoding.
        """
        prehash = f"{timestamp}{method.upper()}{request_path}{body}"
        signature = hmac.new(self.api_secret.encode('utf-8'),
                             prehash.encode('utf-8'),
                             hashlib.sha256).digest()
        return base64.b64encode(signature).decode('utf-8')

    def _get_headers(self, method, request_path, body=""):
        """
        Build the headers needed for authentication.
        """
        timestamp = self._get_timestamp()
        sign = self._generate_sign(timestamp, method, request_path, body)
        headers = {
            "Content-Type": "application/json",
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": sign,
            "ACCESS-PASSPHRASE": self.passphrase,
            "ACCESS-TIMESTAMP": timestamp,
            "locale": "zh-CN"
        }
        return headers

    def _get(self, endpoint, params=None):
        if params:
            query_string = urlencode(params)
            request_path = f"/api/v2/mix/{endpoint}?{query_string}"
        else:
            request_path = f"/api/v2/mix/{endpoint}"
        headers = self._get_headers("GET", request_path, body="")
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, data=None):
        body = json.dumps(data) if data else ""
        request_path = f"/api/v2/mix/{endpoint}"
        headers = self._get_headers("POST", request_path, body=body)
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def fetch_current_price(self, pair):
        symbol = pair.replace('/', '')
        endpoint = "market/ticker"
        params = {
            "symbol": symbol,
            "productType": "usdt-futures"
        }
        data = self._get(endpoint, params=params)
        price = float(data["data"]["last"])
        return price

    def fetch_ohlc(self, pair, interval):
        symbol = pair.replace('/', '')
        endpoint = "market/history-candles"
        granularity = interval * 60
        params = {
            "symbol": symbol,
            "granularity": granularity,
            "limit": 200,
            "productType": "usdt-futures"
        }
        data = self._get(endpoint, params=params)
        candles = data["data"]
        prices = [float(candle[4]) for candle in candles]
        return prices

    def get_balance(self, pair):
        endpoint = "account/accounts"
        params = {"productType": "usdt-futures"}
        data = self._get(endpoint, params=params)
        accounts = data.get("data")
        if not accounts:
            raise Exception(f"No account data returned: {data}")
        # Look for the account where marginCoin equals "USDT"
        usdt_account = next((acc for acc in accounts if acc.get("marginCoin") == "USDT"), None)
        if usdt_account is None:
            raise Exception("USDT account not found in accounts data: " + json.dumps(accounts))
        balance = {
            "base": 0.0,  # For futures, the BTC position is managed separately
            "quote": float(usdt_account.get("available", 0))
        }
        return balance


    def place_order(self, order_type, pair, volume):
        symbol = pair.replace('/', '')
        endpoint = "order/placeOrder"
        order_data = {
            "symbol": symbol,
            "productType": "usdt-futures",
            "marginCoin": "USDT",
            "side": order_type,
            "orderType": "market",
            "size": volume,
        }
        data = self._post(endpoint, data=order_data)
        return data
