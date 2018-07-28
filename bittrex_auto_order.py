import sys
import time
import os
import requests
import hmac
import hashlib
import math
import decimal
import msvcrt
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
        Config.logging = Config.LoggingModes.OFF
        self.menus = Menus()
        self.ui = UserInterface(self.menus)
        self.api_key = BittrexOrderer.read_api_key()
        self.secret_key = BittrexOrderer.read_secret_key()

    def run(self):
        self.ui.run()
        while not self.menus.main_menu.items["Exit"].is_activated:
            if self.menus.main_menu.items["Print Open Orders"].is_activated:
                self.menus.main_menu.items["Print Open Orders"].is_activated = False
                self.ui.disconnect()
                os.system("cls")
                self.print_detailed_open_order_stats()
                print ("Press any key to continue...")
                Utils.wait_for_any_key()
                self.ui.run()
            time.sleep(0.25)  # make sure python doesn't want to kill itself

        os.system("cls")
        print("See you next time!")
        sys.exit()



    def print_detailed_open_order_stats(self):
        open_orders = self.look_up_open_orders()
        for order in open_orders:
            currency = Utils.get_currency_from_exchange(order.exchange)
            balance = self.get_balance(currency)
            self.print_order_stats(order, balance)


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
        return hmac.new(secret_key, url.encode(), hashlib.sha512).hexdigest()

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



bittrex_orderer = BittrexOrderer()
bittrex_orderer.run()
#
# print ("\nAttempting to lookup orders"
# r = BittrexOrderer.send_request("https://bittrex.com/api/v1.1/market/getopenorders?apikey="+api_key)
# open_orders = Utilities.process_open_orders(r.json())
#
# #remove any crytos that have pending open orders
# requested_orders_minus_open_orders = copy.copy(requested_orders)
# count = 1
# print '\n'
# for holding_crypto in requested_orders:
#     for order in open_orders:
#         if holding_crypto.market == order.market:
#             print str(count) + ". Open order already exists on " + order.market + ".\tCancel this order if you want to renew it."
#             count = count + 1
#             requested_orders_minus_open_orders.remove(holding_crypto)
#             break
#
#
# r = BittrexOrderer.send_request("https://bittrex.com/api/v1.1/account/getbalances?apikey="+api_key+"&nonce=")
# balances = Utilities.process_balances(r.json())
#
# # remove any orders that we currently don't have any balance for
# orders_to_place = copy.copy(requested_orders_minus_open_orders)
# count = 1
# for order in requested_orders_minus_open_orders:
#     if "USDT" in order.market.upper(): # not processing any orders bought with USDT
#         print str(count) + "Removing " + order.market
#         count = count + 1
#         orders_to_place.remove(order)
#         continue
#
#     crypto_exists_with_balance = False
#     for balance in balances:
#         if order.market.split('-')[1] == balance.currency:
#             crypto_exists_with_balance = True
#     if not crypto_exists_with_balance:
#         print str(count) + "Removing 0 balance crypto:" + order.market
#         count = count + 1
#         orders_to_place.remove(order)
#
# for order in orders_to_place:
#     BittrexOrderer.place_order(order)
#
# print ("Exiting....."
