import sys
import os
import threading
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
        self.exit_lock = threading.Lock()
        Config.logging = Config.LoggingModes.OFF
        self.menus = Menus()
        self.initialize_menu_item_callback_functions(self.menus)
        self.ui = UserInterface(self.menus)
        self.api_controller = ApiController()

    def run(self):
        self.ui.run(self.menus.main_menu)
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
        self.api_controller.print_detailed_open_order_stats()
        self.ui.wait_for_any_key(self.menus.orders_menu)

    def on_print_balances_activated(self):
        self.api_controller.print_detailed_balance_stats()
        self.ui.wait_for_any_key(self.menus.orders_menu)

    def on_place_orders_activated(self):
        # TODO - do this function
        self.ui.wait_for_any_key(self.menus.orders_menu)

    def on_exit_activated(self):
        self.exit_lock.release() # allow exit


try:
    bittrex_orderer = BittrexOrderer()
    bittrex_orderer.run()
except Exception, ex:
    Utils.log("Fatal error", Config.LoggingModes.FATAL, ex)
    sys.exit()  # let's get the hell outta here!
