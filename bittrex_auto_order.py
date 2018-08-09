import sys
import os
import thread
import threading
from bin.utils import Utils
from bin.configuration import Config
from bin.user_interface import UserInterface
from bin.menus import Menus
from bin.api_controller import ApiController
from bin.configuration_controller import ConfigController

class BittrexOrderer:
    pending_orders = {}
    complete_orders = {}

    def __init__(self):
        print ("Initializing")
        self.exit_lock = threading.Lock()
        self.menus = Menus()
        self.initialize_menu_item_callback_functions(self.menus)
        self.ui = UserInterface(self.menus, handle_fatal_exception)
        self.api_controller = ApiController()
        self.config_controller = ConfigController()

    def run(self):
        self.ui.run(self.menus.main_menu)
        self.exit_lock.acquire() # acquire lock for the first time
        # try to acquire again - will only be released when user requests to exit application
        self.exit_lock.acquire()
        os.system("cls")
        print("See you next time!")
        sys.exit()

    def initialize_menu_item_callback_functions(self, menus):
        # Main
        menus.main_menu.items["Orders"].callback = lambda: self.on_orders_activated()
        menus.main_menu.items["Configuration"].callback = lambda: self.on_config_activated()
        menus.main_menu.items["Exit"].callback = lambda: self.on_exit_activated()
        # Orders
        menus.orders_menu.items["Print Open Orders"].callback = lambda: self.on_print_open_orders_activated()
        menus.orders_menu.items["Print Balances"].callback = lambda: self.on_print_balances_activated()
        menus.orders_menu.items["Place Orders"].callback = lambda: self.on_place_orders_activated()
        menus.orders_menu.items["Back"].callback = lambda: self.on_first_tier_menu_back_activated()
        # Config
        menus.configuration.items["Enter New API Key"].callback = lambda: self.on_write_api_key_activated()
        menus.configuration.items["Print API Key"].callback = lambda: self.on_view_api_key_activated()
        menus.configuration.items["Enter New Secret Key"].callback = lambda: self.on_write_secret_key_activated()
        menus.configuration.items["Print Secret Key"].callback = lambda: self.on_view_secret_key_activated()
        menus.configuration.items["Back"].callback = lambda: self.on_first_tier_menu_back_activated()

    # Main menu items
    def on_orders_activated(self):
        self.ui.run(self.menus.orders_menu)

    def on_config_activated(self):
        self.ui.run(self.menus.configuration)

    def on_exit_activated(self):
        self.exit_lock.release() # allow exit

     # First tier common items
    def on_first_tier_menu_back_activated(self):
        self.ui.run(self.menus.main_menu)

    # Orders items
    def on_print_open_orders_activated(self):
        self.api_controller.print_detailed_open_order_stats()
        self.ui.wait_for_any_key(self.menus.orders_menu)

    def on_print_balances_activated(self):
        self.api_controller.print_detailed_balance_stats()
        self.ui.wait_for_any_key(self.menus.orders_menu)

    def on_place_orders_activated(self):
        # TODO - do this function
        self.ui.wait_for_any_key(self.menus.orders_menu)

    # Configuration items
    def on_write_api_key_activated(self):
        self.config_controller.update_api_key()
        self.ui.wait_for_any_key(self.menus.configuration)

    def on_view_api_key_activated(self):
        self.config_controller.view_api_key()
        self.ui.wait_for_any_key(self.menus.configuration)

    def on_write_secret_key_activated(self):
        self.config_controller.update_secret_key()
        self.ui.wait_for_any_key(self.menus.configuration)

    def on_view_secret_key_activated(self):
        self.config_controller.view_secret_key()
        self.ui.wait_for_any_key(self.menus.configuration)


def handle_fatal_exception(ex):
    Utils.log("Fatal error", Config.LoggingModes.FATAL, ex)
    print("Application will now close. Check logs for further details")
    os._exit(1)  # let's get the hell outta here!

try:
    bittrex_orderer = BittrexOrderer()
    bittrex_orderer.run()
except Exception, ex:
    handle_fatal_exception(ex)
