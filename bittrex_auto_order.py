import sys
import time
import os
import requests
import hmac
import hashlib
import math
import decimal
import msvcrt
import threading
from bin.utils import Utils
from bin.configuration import Config
from bin.user_interface import UserInterface
from bin.menus import Menus

EXPECTED_API_KEY_LENGTH = 32
EXPECTED_SECRET_KEY_LENGTH = 32
# create a new context for this task
ctx = decimal.Context()

# 20 digits should be enough for everyone :D
ctx.prec = 20

def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

class BittrexOrderer:
    pending_orders = {}
    complete_orders = {}

    def __init__(self):
        print ("Initializing")
        self.exit_lock = threading.Lock()
        Config.logging = Config.LoggingModes.OFF
        self.menus = Menus()
        self.initialize_menu_item_callback_functions(self.menus)
        self.ui = UserInterface(self.menus)
        self.api_key = BittrexOrderer.read_api_key()
        self.secret_key = BittrexOrderer.read_secret_key()

    def run(self):
        self.ui.run(
            self.menus.main_menu)
        self.exit_lock.acquire() # acquire lock for the first time
        # try to acquire again - will only be released when user requests to exit application
        self.exit_lock.acquire()
        os.system("cls")
        print("See you next time!")
        sys.exit()

    def initialize_menu_item_callback_functions(self, menus):
        menus.main_menu.items["Orders"].callback = lambda: self.on_orders_activated()
        menus.orders_menu.items["Back"].callback = lambda: self.on_orders_back_activated()
        menus.orders_menu.items["Print Open Orders"].callback = lambda: self.on_print_open_orders_activated()
        menus.orders_menu.items["Print Balances"].callback = lambda: self.on_print_balances_activated()
        menus.orders_menu.items["Place Orders"].callback = lambda: self.on_place_orders_activated()
        menus.main_menu.items["Exit"].callback = lambda: self.on_exit_activated()

    def on_orders_activated(self):
        self.ui.run(self.menus.orders_menu)

    def on_orders_back_activated(self):
        self.ui.run(self.menus.main_menu)

    def on_print_open_orders_activated(self):
        self.print_detailed_open_order_stats()
        print("Press any key to continue...")
        Utils.wait_for_any_key()
        self.ui.run(self.menus.orders_menu)

    def on_print_balances_activated(self):
        self.print_detailed_balance_stats()
        print("Press any key to continue...")
        Utils.wait_for_any_key()
        self.ui.run(self.menus.orders_menu)

    def on_place_orders_activated(self):
        # TODO - do this function
        print("Press any key to continue...")
        Utils.wait_for_any_key()
        self.ui.run(self.menus.orders_menu)

    def on_exit_activated(self):
        self.exit_lock.release() # allow exit

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
        Utils.log("\nAttempting to lookup orders", Config.LoggingModes.INFO)
        r = self.send_request("https://bittrex.com/api/v1.1/market/getopenorders?apikey="+self.api_key)
        return Utils.process_open_orders(r.json())

    @staticmethod
    def read_api_key():
        f = open('api_key', 'r')
        contents = f.read()
        if len(contents) != EXPECTED_API_KEY_LENGTH:
            Utils.log("API Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents)), Config.LoggingModes.WARN)
        return contents

    @staticmethod
    def read_secret_key():
        f = open('secret_key', 'r')
        contents = f.read()
        if len(contents) != EXPECTED_SECRET_KEY_LENGTH:
            Utils.log("Secret Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents)), Config.LoggingModes.WARN)
        return contents

    @staticmethod
    def create_hash(secret_key, url):
        return hmac.new(bytearray(source=secret_key, encoding='ASCII'), url.encode(), hashlib.sha512).hexdigest()

    def send_request(self, url):
        url = url + "&nonce=" + str(int(time.time()))
        hmac_hash = BittrexOrderer.create_hash(self.secret_key, url)
        headers = {'apisign': hmac_hash}
        return requests.get(url, headers=headers)

    @staticmethod
    def send_public_request(url):
        return requests.get(url)

    @staticmethod
    def get_market_summary(market):
        response = BittrexOrderer.send_public_request("https://bittrex.com/api/v1.1/public/getmarketsummary?market=" + market)
        return Utils.process_market_summaries(response.json())


    def place_order(self,order):
        market_summary = BittrexOrderer.get_market_summary(order.market)
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
           + "\n\t-\tQuantity:................ " + float_to_str(order.sell_quantity) + "\tof\t" + float_to_str(order.quantity)
           + "\n\t-\tSell Price:.............. " + float_to_str(order.sell_price)
           + "\n\t-\tReturn:.................. " + float_to_str(order.sell_price * order.quantity / 2)
           + "\n\t-\tCurrent Price:........... " + float_to_str(high)
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
        market_summary = BittrexOrderer.get_market_summary(open_order.exchange)
        if market_summary is None:
            Utils.log("Could not retrieve market summary for " + open_order.exchange, Config.LoggingModes.ERROR)
            return
        high = float(market_summary.high)
        if high is None or math.isnan(high) or high == 0:
            Utils.log("Could not retrieve high price for " + open_order.exchange, Config.LoggingModes.ERROR)
            return
        print ("\n--------------------------------------------------------------------------------------------------"
           + "\n Statistics of " + open_order.exchange
           + "\n\t-\tQuantity Remaining:...... " + float_to_str(open_order.quantity_remaining) + "\tof\t" + float_to_str(balance.balance)
           + "\n\t-\tSell Price:.............. " + float_to_str(open_order.limit)
           + "\n\t-\tReturn:.................. " + float_to_str(open_order.limit * open_order.quantity_remaining / 2)
           + "\n\t-\tCurrent Price:........... " + float_to_str(high)
           + "\n\t-\tCompletion Percentage:... " + str(round((high / open_order.limit) * 100, 2)) + "%"
           + "\n--------------------------------------------------------------------------------------------------")

try:
    bittrex_orderer = BittrexOrderer()
    bittrex_orderer.run()
except Exception, ex:
    Utils.log("Fatal error", Config.LoggingModes.FATAL, ex)
    sys.exit()  # let's get the hell outta here!
