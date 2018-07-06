import sys
import requests
from bin.splash import Splash
from bin.utilities import Utilities

EXPECTED_API_KEY_LENGTH = 32


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



Splash.print_splash_screen()
b_order = BittrexOrderer()
api_key = b_order.read_api_key()
api_key = Utilities.read_orders_from_file()
