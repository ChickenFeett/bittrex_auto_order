import sys
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
    def read_api_key():
        f = open('secret_key', 'r')
        contents = f.read()
        if len(contents) != EXPECTED_SECRET_KEY_LENGTH:
            print "Warning: Secret Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents))
        return contents

    @staticmethod
    def create_hash(secret_key, url):
        return hmac.new(secret_key, url, hashlib.sha512)

Splash.print_splash_screen()
b_order = BittrexOrderer()
api_key = b_order.read_api_key()
secret_key = b_order.read_secret_key()
orders = Utilities.read_orders_from_file()
existing_orders = b_order.get_existing_orders(secret_key)
for order in orders:
    print (order.crypto_type + "\t|\t" + order.quantity + "\t|\t" + order.buy_cost)
