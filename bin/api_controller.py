import time
import requests
import hmac
import hashlib
import math
from bin.utils import Utils
from bin.configuration import Config, LoggingModes
from bin.order_controller import OrderController


class ApiController:
    def __init__(self, order_controller):
        self.api_key = ApiController.read_api_key()
        self.secret_key = ApiController.read_secret_key()
        self.order_controller = order_controller

    def refresh_keys(self):
        self.api_key = ApiController.read_api_key()
        self.secret_key = ApiController.read_secret_key()

    # Looks up open orders via API and prints them to console
    def print_detailed_open_order_stats(self):
        open_orders = self.look_up_open_orders()
        if open_orders is None:
            Utils.log("Failed to retrieve open orders", LoggingModes.ERROR)
            return
        index = 1
        for order in open_orders:
            currency = Utils.get_currency_from_exchange(order.exchange)
            balance = self.get_balance(currency)
            market_summary = ApiController.get_market_summary(order.exchange)
            self.order_controller.print_open_order_stats(index, order, balance, market_summary)
            index = index + 1

    # Looks up balances and prints them to console
    def print_detailed_balance_stats(self):
        balances = self.get_balances()
        if balances is None:
            Utils.log("Failed to retrieve balances", LoggingModes.ERROR)
            return
        index = 1
        for balance in balances:
            self.order_controller.print_balance(index, balance)
            index = index + 1

    def get_balances(self):
        r = self.send_request(
            "https://bittrex.com/api/v1.1/account/getbalances?apikey=" + self.api_key)
        return Utils.process_balances(r.json())

    def get_balance(self, currency):
        if currency is None:
            return None
        r = self.send_request(
            "https://bittrex.com/api/v1.1/account/getbalance?apikey=" + self.api_key + "&currency=" + currency)
        balances = Utils.process_balances(r.json())
        if type(balances) == list:
            return balances[0]
        return None

    def look_up_open_orders(self):
        Utils.log("Attempting to lookup orders", LoggingModes.INFO)
        r = self.send_request("https://bittrex.com/api/v1.1/market/getopenorders?apikey="+self.api_key)
        return Utils.process_open_orders(r.json())

    @staticmethod
    def read_api_key():
        Utils.log("Reading API Key from disk", LoggingModes.DEBUG)
        f = open('api_key', 'r')
        contents = f.read()
        if len(contents) != Config.EXPECTED_API_KEY_LENGTH:
            Utils.log("API Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents)), LoggingModes.WARN)
        return contents

    @staticmethod
    def read_secret_key():
        Utils.log("Reading Secret Key from disk", LoggingModes.DEBUG)
        f = open('secret_key', 'r')
        contents = f.read()
        if len(contents) != Config.EXPECTED_SECRET_KEY_LENGTH:
            Utils.log("Secret Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents)), LoggingModes.WARN)
        return contents

    @staticmethod
    def create_hash(secret_key, url):
        return hmac.new(secret_key, url.encode(), hashlib.sha512).hexdigest()

    def send_request(self, url):
        url = url + "&nonce=" + str(int(time.time()))
        hmac_hash = ApiController.create_hash(self.secret_key, url)
        headers = {'apisign': hmac_hash}
        Utils.log("Sending request to URL: " + url, LoggingModes.DEBUG)
        return requests.get(url, headers=headers)

    @staticmethod
    def send_public_request(url):
        return requests.get(url)

    @staticmethod
    def get_market_summary(market):
        response = ApiController.send_public_request("https://bittrex.com/api/v1.1/public/getmarketsummary?market=" + market)
        return Utils.process_market_summaries(response.json())

    def place_orders(self, orders):
        if type(orders) is not list:
            Utils.log("Incorrect input type in place_orders function", LoggingModes.ERROR)
        for order in orders:
            self.place_order(order)

    def place_order(self, order):
        market_summary = ApiController.get_market_summary(order.market)
        if market_summary is None:
            Utils.log("Could not retrieve market summary for " + order.market, LoggingModes.WARN)
            return
        high = float(market_summary.high)
        if high is None or math.isnan(high) or high == 0:
            Utils.log("Could not retrieve high price from " + order.market, LoggingModes.WARN)
            return
        if order.sell_price < high:
            Utils.log(order.market +" sell price ( " + str(order.sell_price) +" ) is less than high price ( " + '%f' % (high) +" ) ! ", LoggingModes.ERROR)
            return
        url = "https://bittrex.com/api/v1.1/market/selllimit?apikey="+self.api_key+"&market="+order.market+"&quantity="+str(order.sell_quantity)+"&rate="+str(order.sell_price)
        r = self.send_request(url)
        r = r.json()
        self.order_controller.print_placed_order(r, order, high, url)