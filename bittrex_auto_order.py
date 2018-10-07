import sys
import os
import thread
import threading
from bin.utils import Utils
from bin.configuration import Config, LoggingModes
from bin.user_interface import UserInterface
from bin.menus import Menus
from bin.api_controller import ApiController
from bin.configuration_controller import ConfigController
from bin.order_controller import OrderController


class BittrexOrderer:
    pending_orders = {}
    complete_orders = {}

    def __init__(self):
        Utils.log("Initializing", LoggingModes.ALL)
        self.exit_lock = threading.Lock()
        self.menus = Menus()
        self.initialize_menu_item_callback_functions(self.menus)
        self.ui = UserInterface(self.menus, handle_fatal_exception)
        self.order_controller = OrderController()
        self.api_controller = ApiController(self.order_controller)
        self.config_controller = ConfigController()

    def run(self):
        self.ui.run(self.menus.main_menu)
        while True:
            callback = self.ui.callback_queue.get(True, None)  # blocks until an item is available
            if callback is not None:
                callback()


    def initialize_menu_item_callback_functions(self, menus):
        Utils.log("Hooking Up Menu Item's Callback Lambdas", LoggingModes.DEBUG)
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
        os.system("cls")
        Utils.log("Exiting.....", LoggingModes.ALL)
        print("See you next time!")
        sys.exit()

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
        balances = self.api_controller.get_balances()
        open_orders = self.api_controller.look_up_open_orders()
        orders = self.order_controller.read_and_process_orders_ready_for_placing_sell_order(balances, open_orders)
        index = 1
        filename = self.order_controller.prepare_output_file()
        for order in orders:
            balance = self.api_controller.get_balance(order.crypto)
            market_summary = self.api_controller.get_market_summary(order.market)
            self.order_controller.print_order_stats(index, order, balance, market_summary)
            self.order_controller.append_to_output_file(filename, order, balance, market_summary)
            index = index + 1
        if filename is not None:
            os.system("start " + "output\\" + filename)
        if self.confirm_order():
            self.api_controller.place_orders(orders)
        self.ui.wait_for_any_key(self.menus.orders_menu)

    # Configuration items
    def on_write_api_key_activated(self):
        self.config_controller.update_api_key()
        self.api_controller.refresh_keys()
        self.ui.wait_for_any_key(self.menus.configuration)

    def on_view_api_key_activated(self):
        self.config_controller.view_api_key()
        self.ui.wait_for_any_key(self.menus.configuration)

    def on_write_secret_key_activated(self):
        self.config_controller.update_secret_key()
        self.api_controller.refresh_keys()
        self.ui.wait_for_any_key(self.menus.configuration)

    def on_view_secret_key_activated(self):
        self.config_controller.view_secret_key()
        self.ui.wait_for_any_key(self.menus.configuration)

    def on_refresh_keys(self):
        Utils.log("Reading API and Secret keys", LoggingModes.ALL)
        self.api_controller.refresh_keys()

    def confirm_order(self):
        confirmation = raw_input("Please confirm the placement of orders (y/n): ")
        if confirmation.lower() == 'y':
            return True
        elif confirmation.lower() == 'n':
            return False
        else:
            return self.confirm_order()


def handle_fatal_exception(ex):
    Utils.log("Fatal error", LoggingModes.FATAL, ex)
    print("Application will now close. Check logs for further details")
    os._exit(1)  # let's get the hell outta here!

try:
    bittrex_orderer = BittrexOrderer()
    bittrex_orderer.run()
except Exception, ex:
    handle_fatal_exception(ex)
