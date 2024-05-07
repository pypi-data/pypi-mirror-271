from ast import parse
import hmac
import base64
import hashlib
import json
import re
import time
import requests
from urllib.parse import urlencode
from ttxt.utils import general
from ttxt.base import baseSpotExchange
from ttxt.types import baseTypes

# password is account group, which is required for private api calls and private wss
# naming it "password" to keep creds standard
class ascendex(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, password, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.group = password
        self.category = kwargs["category"] if "category" in kwargs else "cash"  # can also be "margin"
        self.domain_url = "https://ascendex.com"
        self.prefix = "api/pro/v1"
        
    ## Auth
    def hmac_sha256(self, secret, pre_hash_msg):
        return hmac.new(secret.encode('utf-8'), pre_hash_msg.encode('utf-8'), hashlib.sha256).digest()

    def sign(self, msg, secret):
        msg = bytearray(msg.encode("utf-8"))
        hmac_key = base64.b64decode(secret)
        signature = hmac.new(hmac_key, msg, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode("utf-8")
        return signature_b64
    
    def utc_timestamp(self):
        return int(round(time.time() * 1e3))

    def make_auth_headers(self, timestamp, preHashString, apikey, secret):
        # convert timestamp to string   
        if isinstance(timestamp, bytes):
            timestamp = timestamp.decode("utf-8")
        elif isinstance(timestamp, int):
            timestamp = str(timestamp)
        header = {
            "x-auth-key": apikey,
            "x-auth-signature": self.sign(f"{timestamp}+{preHashString}", secret),
            "x-auth-timestamp": timestamp,
        }
        return header
    
    def _signedRequest(self, request_path, method, preHashString, params=None, body=None):
        ts = self.utc_timestamp()
        headers = self.make_auth_headers(ts, preHashString, self.key, self.secret)
        url = f"{self.domain_url}/{self.group}/{self.prefix}/{request_path}"
        if method == "GET":
            try:
                response = requests.get(url, headers=headers, params=params)
                return response.json()
            except Exception as e:
                raise e
        else:
            try:
                response = requests.request(method, url, headers=headers, json=body)
                return response.json()
            except Exception as e:
                raise e
    
    ## parsers
    def _parseBalance(self, balData):
        parsedBal = {"free": {}, "total": {}}
        if balData['code'] != 0: raise Exception(balData['message'])
        data = balData.get("data", None)
        if data is not None:
            for element in data:
                parsedBal['total'][element["asset"]] = element.get('totalBalance', None)
                parsedBal['free'][element["asset"]] = element.get('availableBalance', None)
        return parsedBal

    def _parseCreateOrder(self, order):
        parsedOrder = {}
        if order['code'] != 0: raise Exception(order['message'])
        if "data" in order and "info" in order["data"]:
            parsedOrder["id"] = order['data']["info"]["orderId"]
        elif "id" in order:
            parsedOrder["id"] = order['id']
        parsedOrder["symbol"] = None
        parsedOrder["price"] = None
        parsedOrder["amount"] = None
        parsedOrder["side"] = None
        parsedOrder["timestamp"] = None
        parsedOrder["status"] = None
        parsedOrder["orderJson"] = json.dumps(order)
        return parsedOrder
    
    def _parseCancelorder(self, order):
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        if order['code'] != 0: raise Exception(order['message'])
        if 'data' in order and 'info' in order['data']:
            element = order['data']['info']
            parsedOrder['id'] = element.get("orderId",None)
            parsedOrder['symbol'] = element.get("symbol",None)
            parsedOrder['timestamp'] = element.get("timestamp",None)
            parsedOrder["orderJson"] = json.dumps(element) if element else None
        return parsedOrder
        
    def _parseOpenOrders(self, order):
        parsedOrderList = []
        if order['code'] != 0: raise Exception(order['message'])
        if "data" in order:
            for element in order['data']:
                parsedOrderList.append(self._parseOrder(element))
        return parsedOrderList
    
    def _parseOrder(self, order):
        parsedOrder = {}
        parsedOrder["id"] = order.get('orderId', None)
        parsedOrder["tradeId"] = order.get('orderId', None)
        parsedOrder["symbol"] = order.get('symbol', None)
        parsedOrder["price"] = float(order["price"]) if "price" in order else None 
        parsedOrder["amount"] = float(order["orderQty"]) if "orderQty" in order else None
        parsedOrder["side"] = order['side'].lower() if "side" in order else None
        parsedOrder["timestamp"] = int(order["lastExecTime"]) if "lastExecTime" in order else None
        parsedOrder["status"] = order.get("status", None)
        parsedOrder['takerOrMaker'] = "taker" if order["orderType"] == "Market" else "maker"
        parsedOrder["orderJson"] = json.dumps(order) if order else None 
        return parsedOrder
        
    def _parseFetchOrder(self, order):
        if order['code'] != 0: raise Exception(order['message'])
        parsedOrder = {"id": None, "symbol": None, "price": None, "amount": None, "takerOrMaker": None, "datetime": None, "fee": None, "fee_currency": None,
                       "side": None, "timestamp": None, "status": None}
        if "data" in order and order["data"] != {}:
            order = order['data']
            parsedOrder["id"] = order["orderId"]
            parsedOrder["symbol"] = order["symbol"]
            parsedOrder["price"] = float(order["price"])
            parsedOrder['takerOrMaker'] = order.get('tradeScope', None)
            parsedOrder["amount"] = float(order["orderQty"])
            parsedOrder["side"] = order["side"].lower()
            parsedOrder["timestamp"] = int(order["lastExecTime"])
            parsedOrder["datetime"] = general.ts_to_datetime(parsedOrder["timestamp"])
            parsedOrder["status"] = order.get('status', None)
            parsedOrder["fee_currency"] = order["feeAsset"]
        return parsedOrder
        
        
    def _parseFetchTrades(self, order):
        if order['code'] != 0: raise Exception(order['message'])
        parsedTradesList = []
        if "data" in order and order["data"] != []:
            for element in order['data']:
                parsedTradesList.append(self._parseOrder(element))
        return parsedTradesList
        
    ## Exchange functions
    def fetch_ticker(self, symbol):
        raise NotImplementedError("method not implemented")
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = f'{self.category}/balance'
        params = {"showAll": False}
        preHashString = "balance"
        try:
            resp = self._signedRequest(method="GET", request_path=apiUrl, preHashString=preHashString ,params=params)
            return self._parseBalance(resp)
        except Exception as e:
            raise e
    
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        apiUrl = f'{self.category}/order/hist/current'
        preHashString = "order/hist/current"
        params = {
            "symbol": symbol,
            "executedOnly": True
        }
        if limit:
            params['n'] = limit
        try:
            resp = self._signedRequest(method="GET", request_path=apiUrl, preHashString=preHashString, params=params)
            return self._parseFetchTrades(resp)
        except Exception as e:
            raise e
    
    def create_order(self, symbol, side, amount, order_type, price=None, params={}): 
        try:
            if order_type == "limit":
                return self.create_limit_order(symbol, amount, side, price, params={})
            elif order_type == "market":
                return self.create_market_order(symbol, amount, side, params={})
        except Exception as e:
            raise e
    
    def create_market_order(self, symbol, amount, side, params={}):
        apiUrl = f"{self.category}/order"
        preHashString = "order"
        body = {    
            'account-group': self.group,
            'account-category': self.category,
            'symbol': symbol,
            'time': self.utc_timestamp(),
            'orderQty': str(amount),    
            'orderType': "market",
            'side': side,  # buy or sell,
        }
        try:
            resp = self._signedRequest(method="POST", request_path=apiUrl, preHashString=preHashString, body=body)
            return self._parseCreateOrder(resp)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, amount, side, price, params={}):
        apiUrl = f"{self.category}/order"
        preHashString = "order"
        body = {
            'account-group': self.group,
            'account-category': self.category,
            'symbol': symbol,
            'time': self.utc_timestamp(),
            'orderQty': str(amount),
            'orderPrice': str(price),
            'orderType': "limit",
            'side': side,  # buy or sell,
        }
        try:
            resp = self._signedRequest(method="POST", request_path=apiUrl, preHashString=preHashString, body=body)
            return self._parseCreateOrder(resp)
        except Exception as e:
            raise e
    
    def cancel_order(self, id=None, symbol=None, params={}):
        apiUrl = f"{self.category}/order"
        preHashString = "order"
        try:
            params = {
                "orderId": id,
                "time": self.utc_timestamp()
            }
            if symbol:
                params['symbol'] = symbol
            response = self._signedRequest(method='DELETE', request_path=apiUrl, preHashString=preHashString, body=params)
            return self._parseCancelorder(response)
        except Exception as e:
            raise e
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        apiUrl = f"{self.category}/order/open"
        preHashString="order/open"
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
            response = self._signedRequest(method='GET', request_path=apiUrl, preHashString=preHashString, params=None, body=None)
            return self._parseOpenOrders(response)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol = None, params={}):
        apiUrl = f"{self.category}/order/status"
        preHashString="order/status"
        try:
            params = {
                "orderId": id
            }
            response = self._signedRequest(method='GET', request_path=apiUrl, preHashString=preHashString, params=params, body=None)
            return self._parseFetchOrder(response)
        except Exception as e:
            raise e
        
# https://ascendex.github.io/ascendex-pro-api/#generate-order-id
# https://github.com/ascendex/ascendex-pro-api-demo/blob/main/signature_demo/python/signature.py