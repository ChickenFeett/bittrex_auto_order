import sys
import time
import copy
import requests
from bin.splash import Splash
from bin.utilities import Utilities
import hmac
import hashlib
import math

EXPECTED_API_KEY_LENGTH = 32
EXPECTED_SECRET_KEY_LENGTH = 32


class BittrexOrderer:
    pending_orders = {}
    complete_orders = {}

    def __init__(self):
        print "Initializing"

    @staticmethod
    def read_api_key():
        f = open('api_key', 'r')
        contents = f.read()
        if len(contents) != EXPECTED_API_KEY_LENGTH:
            print "Warning: API Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents))
        return contents

    @staticmethod
    def read_secret_key():
        f = open('secret_key', 'r')
        contents = f.read()
        if len(contents) != EXPECTED_SECRET_KEY_LENGTH:
            print "Warning: Secret Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents))
        return contents

    @staticmethod
    def create_hash(secret_key, url):
        return hmac.new(secret_key, url, hashlib.sha512).hexdigest()

    @staticmethod
    def send_request(url):
        url = url + "&nonce=" + str(int(time.time()))
        hmac_hash = b_order.create_hash(secret_key, url)
        headers = {'apisign': hmac_hash}
        return requests.get(url, headers=headers)

    @staticmethod
    def send_public_request(url):
        return requests.get(url)

    @staticmethod
    def get_market_summary(market):
        response = BittrexOrderer.send_public_request("https://bittrex.com/api/v1.1/public/getmarketsummary?market=" + market)
        return Utilities.construct_market_summary_from_json(response.json())

    @staticmethod
    def place_order(order):
        market_summary = BittrexOrderer.get_market_summary(order.market)
        if market_summary is None:
            print "ERROR: Could not retrieve market summary for " + order.market
            return
        high = float(market_summary.high)
        if high is None or math.isnan(high) or high == 0:
            print "ERROR: Could not retrieve high price from " + order.market
            return
        if order.sell_price < high:
            print "ERROR: "+order.market+" sell price ( "+str(order.sell_price)+" ) is less than high price ( "+ '%f' % (high) +" ) ! "
            return
        r = BittrexOrderer.send_request("https://bittrex.com/api/v1.1/market/selllimit?apikey="+api_key+"&market="+order.market+"&quantity="+str(order.quantity)+"&rate="+str(order.sell_price))
        r = r.json()
        print ("\n--------------------------------------------------------------------------------------------------"
           + "\nPlacing order.py on " + order.market
           + "\n\t-\tQuantity:................ " + str(order.quantity / 2) + "\tof\t" + str(order.quantity)
           + "\n\t-\tPrice:................... " + str(order.sell_price)
           + "\n\t-\tReturn:.................. " + str(order.sell_total)
           + "\n\t-\tCurrent Price:........... " + str('%f' % (high))
           + "\n\t-\tDistance %:.............. " + str(round((high / order.sell_price) * 100, 2)) + "%"
           + "\n--------------------------------------------------------------------------------------------------\n")
        if "success" in r:
            if r['success'] == 'true':
                print "            SUCCESS             \n"
            elif 'message' in r:
                print " * *      F A I L E D ! : " + r['message'] + "        * * \n"
            else:
                print " * *      F A I L E D !     * * \n"
        else:
            print " * *      F A I L E D !     * * \n"


Splash.print_splash_screen()
b_order = BittrexOrderer()
api_key = b_order.read_api_key()
secret_key = b_order.read_secret_key()
requested_orders = Utilities.read_orders_from_file()
nonce = str(int(time.time()))
for holding_crypto in requested_orders:
    print (holding_crypto.market + "\t|\t" + str(holding_crypto.quantity) + "\t|\t" + str(holding_crypto.buy_cost))

print "Attempting to lookup orders"
r = b_order.send_request("https://bittrex.com/api/v1.1/market/getopenorders?apikey="+api_key)
print r.status_code
print r.json()
open_orders = Utilities.read_orders_from_json(r.json())

print "\t Market |\t Quantity \t|\t Cost"
for order in open_orders:
    print (order.market + "\t|\t" + str(order.quantity) + "\t|\t" + str(order.buy_cost))
# remove any crytos that have pending open orders
requested_orders_minus_open_orders = copy.copy(requested_orders)
for holding_crypto in requested_orders:
    for order in open_orders:
        if holding_crypto.market == order.market:
            print ("found match " + order.market)
            requested_orders_minus_open_orders.remove(holding_crypto)
            break


r = b_order.send_request("https://bittrex.com/api/v1.1/account/getbalances?apikey="+api_key+"&nonce=")
balances = Utilities.read_balances_from_json(r.json())

# remove any orders that we currently don't have any balance for
orders_to_place = copy.copy(requested_orders_minus_open_orders)
for order in requested_orders_minus_open_orders:
    if "USDT" in order.market.upper(): # not processing any orders bought with USDT
        orders_to_place.remove(order)
        continue
    crypto_exists = False
    for balance in balances:
        if order.market.split('-')[1] == balance.currency:
            crypto_exists = True
    if not crypto_exists:
        orders_to_place.remove(order)

for order in orders_to_place:
    BittrexOrderer.place_order(order)


print "Exiting....."
