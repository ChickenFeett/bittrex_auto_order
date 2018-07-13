import csv
from crypto import Crypto
from definitions import Definition

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
        return orders

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
            order = Utilities.create_open_orders(result, rows_processed)
            if order is not None:
                orders.append(order)
            rows_processed = rows_processed + 1
        print str(rows_processed) + " records read"
        print str(len(orders)) + " open orders found"
        return orders

    @staticmethod
    def create_open_orders(response, index):
        if Utilities.valid_open_orders(response):
            return Crypto(index + 1,
                          response[Definition.api_key_Exchange],
                          response[Definition.api_key_Quantity],
                          response[Definition.api_key_Limit],
                          response[Definition.api_key_Price])
        return None

    @staticmethod
    def valid_open_orders(response):
        return (Definition.api_key_OrderUuid in response
            and Definition.api_key_QuantityRemaining in response
            and Definition.api_key_IsConditional in response
            and Definition.api_key_ImmediateOrCancel in response
            and Definition.api_key_Uuid in response
            and Definition.api_key_Exchange in response
            and Definition.api_key_OrderType in response
            and Definition.api_key_Price in response
            and Definition.api_key_CommissionPaid in response
            and Definition.api_key_Opened in response
            and Definition.api_key_Limit in response
            and Definition.api_key_Closed in response
            and Definition.api_key_ConditionTarget in response
            and Definition.api_key_CancelInitiated in response
            and Definition.api_key_PricePerUnit in response
            and Definition.api_key_Condition in response
            and Definition.api_key_Quantity in response)

    @staticmethod
    def create_order_from_csv(row, index):
        if Utilities.csv_row_is_valid_buy_order(row):
            return Crypto(index + 1,
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
                and row[Definition.csv_key_type] == Definition.LIMIT_BUY)
