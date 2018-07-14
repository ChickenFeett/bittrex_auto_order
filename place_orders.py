import sys
import time
import requests
from bin.splash import Splash
from bin.utilities import Utilities
import hmac
import hashlib

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
        url = url + str(int(time.time()))
        hmac_hash = b_order.create_hash(secret_key, url)
        headers = {'apisign': hmac_hash}
        return requests.get(url, headers=headers)



Splash.print_splash_screen()
b_order = BittrexOrderer()
api_key = b_order.read_api_key()
secret_key = b_order.read_secret_key()
holdings = Utilities.read_orders_from_file()
nonce = str(int(time.time()))
for holding_crypto in holdings:
    print (holding_crypto.crypto_type + "\t|\t" + str(holding_crypto.quantity) + "\t|\t" + str(holding_crypto.buy_cost))

print "Attempting to lookup orders"
r = b_order.send_request("https://bittrex.com/api/v1.1/market/getopenorders?apikey="+api_key+"&nonce=")
print r.status_code
print r.json()
open_orders = Utilities.read_orders_from_json(r.json())
for order in open_orders:
    print (order.crypto_type + "\t|\t" + str(order.quantity) + "\t|\t" + str(order.buy_cost))
    for holding_crypto in holdings:
        if holding_crypto.crypto_type == order.crypto_type:
            print ("found match " + order.crypto_type)

print "Exiting....."
