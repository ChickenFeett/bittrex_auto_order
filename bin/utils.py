import csv
import copy
from .openorder import OpenOrder
from .configuration import Config
from .crypto_balance import CryptoBalance
from .order import Order
from .definitions import Definition
from .market_summary import MarketSummary
import msvcrt
import json

SELL_MARK_UP = 2  # 200% mark up
SELL_AMOUNT_DIVIDER = 2 # Only sell half
APPLICATION_LOG_FILE_PATH = "data\\bao.log"

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def wait_for_any_key():
        while msvcrt.kbhit():  # remove any keys in buffer
            msvcrt.getch()
        msvcrt.getch()  # then wait for key press

    @staticmethod
    def get_currency_from_exchange(exchange):
        try:
            return exchange.split('-')[1]
        except IndexError:
            return None

    @staticmethod
    def process_orders():
        orders = []
        with open('input\orders.json', 'r') as file:
            jsonified = json.load(file)
            rows_processed = 0
            if (jsonified is None):
                return None
            for value in jsonified:
                order = Utils.create_order(value, rows_processed)
                if order is not None:
                    orders.append(order)
                rows_processed = rows_processed + 1
        Utils.log(str(len(orders)) + " of " + str(rows_processed) + " orders processed successfully", Config.LoggingModes.INFO)
        return orders

    @staticmethod
    def process_historical_orders():
        orders = []
        with open('input\orders.csv', 'r') as csvfile:
            rows_processed = 0
            csv_file = csv.DictReader(csvfile, delimiter=',')
            if (csv_file is None):
                return None
            for row in csv_file:
                order = Utils.create_order_from_historical(row, rows_processed)
                if order is not None:
                    orders.append(order)
                rows_processed = rows_processed + 1
        Utils.log(str(len(orders)) + " of " + str(rows_processed) + " historical orders processed successfully", Config.LoggingModes.INFO)
        Utils.combine_duplicates(orders)
        Utils.log(str(len(orders)) + " unique buy orders", Config.LoggingModes.INFO)
        return orders

    @staticmethod
    def combine_duplicates(orders, index=0):
        # Process all element up to n - 1
        if index >= (len(orders) - 1):
            return orders

        duplicate = False
        selected_element = orders.pop(index)
        for i in range(index, len(orders)):
            if selected_element.market != orders[i].market:
                continue
            combined_order = Utils.create_combined_order(selected_element, orders[i])
            orders.remove(orders[i])
            orders.append(combined_order)
            new_orders = Utils.combine_duplicates(orders, index)
            duplicate = True
            break
        if duplicate:
            return Utils.combine_duplicates(new_orders, index)
        else:
            orders.insert(index, selected_element)
            return Utils.combine_duplicates(orders, index + 1)


    @staticmethod
    def create_combined_order(order1, order2):
        total_cost = order1.buy_cost + order2.buy_cost
        total_quantity = order1.quantity + order2.quantity
        total_sell_quantity = order1.sell_quantity + order2.sell_quantity
        new_price_per_coin = total_cost / total_quantity
        return Order(order1.order_id, order1.market.split('-')[1], order1.market, total_quantity, total_sell_quantity, new_price_per_coin, total_cost, new_price_per_coin*2)

    # Input: JSONified response from API get open orders
    # Output: Array of orders
    @staticmethod
    def process_open_orders(response):
        orders = []
        rows_processed = 0
        if response is None:
            return None
        if Definition.api_key_result not in response:
            return None
        results = response[Definition.api_key_result]
        if results is None:
            return None
        for result in results:
            order = Utils.create_open_order(result)
            if order is not None:
                orders.append(order)
            rows_processed = rows_processed + 1
        Utils.log(str(len(orders)) + " of " + str(rows_processed) + " open orders processed successfully", Config.LoggingModes.INFO)
        return orders

    @staticmethod
    def process_balances(response):
        balances = []
        rows_processed = 0
        if response is None:
            return None
        if Definition.api_key_result not in response:
            return None
        results = response[Definition.api_key_result]
        if results is None:
            return None
        if type(results) == dict:
            results = [results]
        for result in results:
            order = Utils.get_balance(result, rows_processed)
            if order is not None and order.balance > 0:
                balances.append(order)
            rows_processed = rows_processed + 1
        Utils.log(str(len(balances)) + " of " + str(rows_processed) + " balances processed successfully", Config.LoggingModes.INFO)
        return balances

    @staticmethod
    def get_balance(response, index):
        if Utils.dictionary_contains_keys(response, Definition.api_keys_balance):
            return CryptoBalance(index + 1,
                             response[Definition.api_key_Currency],
                             response[Definition.api_key_Balance],
                             response[Definition.api_key_Available],
                             response[Definition.api_key_Pending],
                             response[Definition.api_key_CryptoAddress])
        return None

    @staticmethod
    def process_market_summaries(response):
        if response is None:
            return None
        if Definition.api_key_result not in response:
            return None
        result = response[Definition.api_key_result]
        if type(result) is list:
            result = result[0]
        if result is None:
            return None
        return Utils.create_market_summary(result)

    @staticmethod
    def create_open_order(response):
        if Utils.dictionary_contains_keys(response, Definition.api_keys_open_orders):
            return OpenOrder(
                response[Definition.api_key_OrderUuid],
                response[Definition.api_key_QuantityRemaining],
                response[Definition.api_key_IsConditional],
                response[Definition.api_key_ImmediateOrCancel],
                response[Definition.api_key_Uuid],
                response[Definition.api_key_Exchange],
                response[Definition.api_key_OrderType],
                response[Definition.api_key_Price],
                response[Definition.api_key_CommissionPaid],
                response[Definition.api_key_Opened],
                response[Definition.api_key_Limit],
                response[Definition.api_key_Closed],
                response[Definition.api_key_ConditionTarget],
                response[Definition.api_key_CancelInitiated],
                response[Definition.api_key_PricePerUnit],
                response[Definition.api_key_Condition],
                response[Definition.api_key_Quantity])
        return None

    @staticmethod
    def create_market_summary(response):
        if Utils.dictionary_contains_keys(response, Definition.api_keys_market_summary):
            return MarketSummary(response[Definition.api_key_MarketName],
                    response[Definition.api_key_High],
                    response[Definition.api_key_Low],
                    response[Definition.api_key_Volume],
                    response[Definition.api_key_Last],
                    response[Definition.api_key_BaseVolume],
                    response[Definition.api_key_TimeStamp],
                    response[Definition.api_key_Bid],
                    response[Definition.api_key_Ask],
                    response[Definition.api_key_OpenBuyOrders],
                    response[Definition.api_key_OpenSellOrders],
                    response[Definition.api_key_PrevDay],
                    response[Definition.api_key_Created])
        return None

    @staticmethod
    def dictionary_contains_keys(response, expected_keys):
        for key in expected_keys:
            if key not in response:
                return False
        return True

    @staticmethod
    def create_order_from_historical(row, index):
        if Utils.dictionary_contains_keys(row, Definition.file_keys_historical_orders):
            if len(row[Definition.csv_key_order_uuid]) == 0 or row[Definition.csv_key_order_uuid].isspace():
                return None
            return Order(index + 1,
                          row[Definition.csv_key_exchange].split('-')[1],
                          row[Definition.csv_key_exchange],
                          row[Definition.csv_key_quantity],
                          float(row[Definition.csv_key_quantity])/SELL_AMOUNT_DIVIDER,
                          row[Definition.csv_key_limit],
                          row[Definition.csv_key_price],
                          float(row[Definition.csv_key_limit])*SELL_MARK_UP)
        return None

    @staticmethod
    def create_order(value, index):
        if Utils.dictionary_contains_keys(value, Definition.file_keys_orders):
            return Order(index + 1,
                         value[Definition.file_key_crypto],
                         value[Definition.file_key_market],
                         value[Definition.file_key_quantity],
                         value[Definition.file_key_sell_quantity],
                         value[Definition.file_key_buy_price],
                         value[Definition.file_key_buy_cost],
                         value[Definition.file_key_sell_price])
        return None

    @staticmethod
    def log(msg, mode, ex=None):
        Utils.log_to_file(msg, mode, ex)
        if Config.logging == Config.LoggingModes.OFF:  # 0
            return
        elif Config.logging == Config.LoggingModes.FATAL and mode == Config.LoggingModes.FATAL:  # 1
            print("FATAL - " + msg)
            return
        elif Config.logging == Config.LoggingModes.ERROR and mode <= Config.LoggingModes.ERROR:  # 2
            print("ERROR - " + msg)
            return
        elif Config.logging == Config.LoggingModes.WARN and mode <= Config.LoggingModes.WARN:  # 3
            print("WARNING - " + msg)
            return
        elif Config.logging == Config.LoggingModes.INFO and mode <= Config.LoggingModes.INFO:  # 4
            print("INFO - " + msg)
            return
        elif Config.logging == Config.LoggingModes.DEBUG and mode <= Config.LoggingModes.DEBUG:  # 5
            print("DEBUG - " + msg)
            return
        elif Config.logging == Config.LoggingModes.TRACE and mode <= Config.LoggingModes.TRACE:  # 6
            print("TRACE - " + msg)
            return
        else:  # 7
            print("ALL - " + msg)

    @staticmethod
    def log_to_file(msg, mode, ex):
        try:
            with open(APPLICATION_LOG_FILE_PATH) as f:
                if type(ex) is str:
                    ex = '\n' + ex
                else:
                    ex = ''
                f.write(str(mode) + ": " + str(msg) + str(ex))
                f.close()
        except Exception, logging_exception:
            if type(ex) is Exception:
                raise ex # raise original exception, if present - it's the reason we're here anyway.
            raise logging_exception # otherwise re-raise most current exception
