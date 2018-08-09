import sys
import time
import os
from bin.utils import Utils
from bin.configuration import Config
from bin.user_interface import UserInterface
from bin.menus import Menus
from bin.apicontroller import ApiController


class BittrexOrderer:
    pending_orders = {}
    complete_orders = {}

    def __init__(self):
        print ("Initializing")
        Config.logging = Config.LoggingModes.OFF
        self.menus = Menus()
        self.ui = UserInterface(self.menus)
        self.api_controller = ApiController()

    def run(self):
        self.ui.run()
        while not self.menus.main_menu.items["Exit"].is_activated:
            if self.menus.main_menu.items["Print Open Orders"].is_activated:
                self.menus.main_menu.items["Print Open Orders"].is_activated = False
                self.ui.disconnect()
                os.system("cls")
                self.api_controller.print_detailed_open_order_stats()
                print ("Press any key to continue...")
                self.ui.wait_for_any_key()
                self.ui.run()
            time.sleep(0.25)  # make sure python doesn't want to kill itself

        os.system("cls")
        print("See you next time!")
        sys.exit()



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
