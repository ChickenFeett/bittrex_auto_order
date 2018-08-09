import time
import requests
import hmac
import hashlib
import math
from bin.utils import Utils
from bin.configuration import Config

class ApiController:
    def __init__(self):
        self.api_key = ApiController.read_api_key()
        self.secret_key = ApiController.read_secret_key()

    def print_detailed_open_order_stats(self):
        open_orders = self.look_up_open_orders()
        if open_orders is None:
            Utils.log("Failed to retrieve open orders", Config.LoggingModes.ERROR)
            return
        for order in open_orders:
            currency = Utils.get_currency_from_exchange(order.exchange)
            balance = self.get_balance(currency)
            self.print_order_stats(order, balance)

    def print_detailed_balance_stats(self):
        balances = self.get_balances()
        if balances is None:
            Utils.log("Failed to retrieve balances", Config.LoggingModes.ERROR)
            return
        for balance in balances:
            # TODO - Make this print pretty stats
            print (balance)

    def get_balances(self):
        # TODO - implement this function
        return None

    def get_balance(self, currency):
        if currency is None:
            return None
        r = self.send_request(
            "https://bittrex.com/api/v1.1/account/getbalance?apikey=" + self.api_key + "&currency=" + currency + "&nonce=")
        balances = Utils.process_balances(r.json())
        if type(balances) == list:
            return balances[0]
        return None

    def look_up_open_orders(self):
        Utils.log("Attempting to lookup orders", Config.LoggingModes.INFO)
        r = self.send_request("https://bittrex.com/api/v1.1/market/getopenorders?apikey="+self.api_key)
        return Utils.process_open_orders(r.json())

    @staticmethod
    def read_api_key():
        f = open('api_key', 'r')
        contents = f.read()
        if len(contents) != Config.EXPECTED_API_KEY_LENGTH:
            Utils.log("API Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents)), Config.LoggingModes.WARN)
        return contents

    @staticmethod
    def read_secret_key():
        f = open('secret_key', 'r')
        contents = f.read()
        if len(contents) != Config.EXPECTED_SECRET_KEY_LENGTH:
            Utils.log("Secret Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents)), Config.LoggingModes.WARN)
        return contents

    @staticmethod
    def create_hash(secret_key, url):
        return hmac.new(secret_key, url.encode(), hashlib.sha512).hexdigest()

    def send_request(self, url):
        url = url + "&nonce=" + str(int(time.time()))
        hmac_hash = ApiController.create_hash(self.secret_key, url)
        headers = {'apisign': hmac_hash}
        return requests.get(url, headers=headers)

    @staticmethod
    def send_public_request(url):
        return requests.get(url)

    @staticmethod
    def get_market_summary(market):
        response = ApiController.send_public_request("https://bittrex.com/api/v1.1/public/getmarketsummary?market=" + market)
        return Utils.process_market_summaries(response.json())


    def place_order(self,order):
        market_summary = ApiController.get_market_summary(order.market)
        if market_summary is None:
            Utils.log("Could not retrieve market summary for " + order.market, Config.LoggingModes.WARN)
            return
        high = float(market_summary.high)
        if high is None or math.isnan(high) or high == 0:
            Utils.log("Could not retrieve high price from " + order.market, Config.LoggingModes.WARN)
            return
        if order.sell_price < high:
            Utils.log("ERROR: " + order.market +" sell price ( " + str(order.sell_price) +" ) is less than high price ( " + '%f' % (high) +" ) ! ", Config.LoggingModes.WARN)
            return
        url = "https://bittrex.com/api/v1.1/market/selllimit?apikey="+self.api_key+"&market="+order.market+"&quantity="+str(order.sell_quantity)+"&rate="+str(order.sell_price)
        r = self.send_request(url)
        r = r.json()
        print ("\n--------------------------------------------------------------------------------------------------"
           + "\nPlacing order on " + order.market
           + "\n\t-\tQuantity:................ " + Utils.float_to_str(order.sell_quantity) + "\tof\t" + Utils.float_to_str(order.quantity)
           + "\n\t-\tSell Price:.............. " + Utils.float_to_str(order.sell_price)
           + "\n\t-\tReturn:.................. " + Utils.float_to_str(order.sell_price * order.quantity / 2)
           + "\n\t-\tCurrent Price:........... " + Utils.float_to_str(high)
           + "\n\t-\tCompletion Percentage:... " + str(round((high / order.sell_price) * 100, 2)) + "%"
           + "\n--------------------------------------------------------------------------------------------------")
        if "success" in r:
            if r['success'] or r['success']  == 'true':
                print ("                            ! ! ! ! !       SUCCESS         ! ! ! ! !                        ")
            elif 'message' in r and len(r['message']) != 0 and not str(r['message']).isspace():
                print ("                            * * * * *     F A I L E D !     ->  " + r['message'] + "         ")
            else:
                print ("                            * * * * *     F A I L E D !     * * * * *                            ")
        else:
            print ("                            * * * * *     F A I L E D !     * * * * *                            ")
        print (url + "\n--------------------------------------------------------------------------------------------------\n")

    def print_order_stats(self, open_order, balance):
        if open_order is None:
            Utils.log("Could not print stats - failed to retrieve order", Config.LoggingModes.ERROR)
            return
        if balance is None:
            Utils.log("Could not print stats - failed to retrieve balance", Config.LoggingModes.ERROR)
            return
        market_summary = ApiController.get_market_summary(open_order.exchange)
        if market_summary is None:
            Utils.log("Could not retrieve market summary for " + open_order.exchange, Config.LoggingModes.ERROR)
            return
        high = float(market_summary.high)
        if high is None or math.isnan(high) or high == 0:
            Utils.log("Could not retrieve high price for " + open_order.exchange, Config.LoggingModes.ERROR)
            return
        print ("\n--------------------------------------------------------------------------------------------------"
           + "\n Statistics of " + open_order.exchange
           + "\n\t-\tQuantity Remaining:...... " + Utils.float_to_str(open_order.quantity_remaining) + "\tof\t" + Utils.float_to_str(balance.balance)
           + "\n\t-\tSell Price:.............. " + Utils.float_to_str(open_order.limit)
           + "\n\t-\tReturn:.................. " + Utils.float_to_str(open_order.limit * open_order.quantity_remaining / 2)
           + "\n\t-\tCurrent Price:........... " + Utils.float_to_str(high)
           + "\n\t-\tCompletion Percentage:... " + str(round((high / open_order.limit) * 100, 2)) + "%"
           + "\n--------------------------------------------------------------------------------------------------")

