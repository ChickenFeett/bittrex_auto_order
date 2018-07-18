import csv
import copy
from crypto import Crypto
from crypto_balance import CryptoBalance
from order import Order
from definitions import Definition
from market_summary import MarketSummary


class Utilities:
    def __init__(self):
        pass

    @staticmethod
    def read_orders_from_file():
        orders = []
        with open('input\orders.csv', 'r') as csvfile:
            rows_processed = 0
            csv_file = csv.DictReader(csvfile, delimiter=',')
            if (csv_file is None):
                return None
            for row in csv_file:
                order = Utilities.create_order_from_csv(row, rows_processed)
                if order is not None:
                    orders.append(order)
                rows_processed = rows_processed + 1
        print str(rows_processed) + " records read"
        print str(len(orders)) + " buy orders found"
        Utilities.combine_duplicates(orders)
        print str(len(orders)) + " unique buy orders"
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
            combined_order = Utilities.create_combined_order(selected_element, orders[i])
            orders.remove(orders[i])
            orders.append(combined_order)
            new_orders = Utilities.combine_duplicates(orders, index)
            duplicate = True
            break
        if duplicate:
            return Utilities.combine_duplicates(new_orders, index)
        else:
            orders.insert(index, selected_element)
            return Utilities.combine_duplicates(orders, index + 1)


    @staticmethod
    def create_combined_order(order1, order2):
        total_cost = order1.buy_cost + order2.buy_cost
        total_quantity = order1.quantity + order2.quantity
        new_price_per_coin = total_cost / total_quantity
        return Order(order1.order_id, order1.market, total_quantity, new_price_per_coin,
                                total_cost)

    @staticmethod
    def read_orders_from_json(response):
        orders = []
        rows_processed = 0
        if response is None:
            return None
        if Definition.api_key_result not in response:
            return None
        results = response[Definition.api_key_result]
        for result in results:
            order = Utilities.get_open_orders(result, rows_processed)
            if order is not None:
                orders.append(order)
            rows_processed = rows_processed + 1
        print str(rows_processed) + " records read"
        print str(len(orders)) + " open orders found"
        return orders

    @staticmethod
    def read_balances_from_json(response):
        balances = []
        rows_processed = 0
        if response is None:
            return None
        if Definition.api_key_result not in response:
            return None
        results = response[Definition.api_key_result]
        for result in results:
            order = Utilities.get_balance(result, rows_processed)
            if order is not None and order.balance > 0:
                balances.append(order)
            rows_processed = rows_processed + 1
        print str(rows_processed) + " records read"
        print str(len(balances)) + " open orders found"
        return balances

    @staticmethod
    def get_balance(response, index):
        if Utilities.valid_api_response(response, Definition.api_keys_balance):
            return CryptoBalance(index + 1,
                             response[Definition.api_key_Currency],
                             response[Definition.api_key_Balance],
                             response[Definition.api_key_Available],
                             response[Definition.api_key_Pending],
                             response[Definition.api_key_CryptoAddress])
        return None

    @staticmethod
    def construct_market_summary_from_json(response):
        if response is None:
            return None
        if Definition.api_key_result not in response:
            return None
        result = response[Definition.api_key_result]
        if type(result) is list:
            result = result[0]
        if result is None:
            return None
        return Utilities.create_market_summary(result)

    @staticmethod
    def get_open_orders(response, index):
        if Utilities.valid_api_response(response, Definition.api_keys_open_orders):
            return Crypto(index + 1,
                          response[Definition.api_key_Exchange],
                          response[Definition.api_key_Quantity],
                          response[Definition.api_key_Limit],
                          response[Definition.api_key_Price])
        return None

    @staticmethod
    def create_market_summary(response):
        if Utilities.valid_api_response(response, Definition.api_keys_market_summary):
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
    def valid_api_response(response, expected_keys):
        for key in expected_keys:
            if key not in response:
                return False
        return True

    @staticmethod
    def create_order_from_csv(row, index):
        if Utilities.csv_row_is_valid_buy_order(row):
            return Order(index + 1,
                          row[Definition.csv_key_exchange],
                          row[Definition.csv_key_quantity],
                          row[Definition.csv_key_limit],
                          row[Definition.csv_key_price])
        return None

    @staticmethod
    def csv_row_is_valid_buy_order(row):
        return (Definition.csv_key_exchange in row
                and Definition.csv_key_type
                and Definition.csv_key_quantity in row
                and Definition.csv_key_limit in row
                and Definition.csv_key_price in row
                and row[Definition.csv_key_type] == Definition.LIMIT_BUY) # DO NOT PROCESS SELL ORDERS
