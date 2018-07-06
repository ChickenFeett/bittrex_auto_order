import csv
from order import Order


class Utilities:
    key_order_uuid = "OrderUuid"
    key_exchange = "Exchange"
    key_type = "Type"
    key_quantity = "Quantity"
    key_limit = "Limit"
    key_commission_paid = "CommissionPaid"
    key_price = "Price"
    key_opened = "Opened"
    key_closed = "Closed"

    LIMIT_BUY = "LIMIT_BUY"
    LIMIT_SELL = "LIMIT_SELL"

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
                order = Utilities.create_order(row, rows_processed)
                if order is not None:
                    orders.append(order)
                rows_processed = rows_processed + 1
        print str(rows_processed) + " records read"
        print str(len(orders)) + " buy orders found"

    @staticmethod
    def create_order(row, index):
        if Utilities.row_is_valid_buy_order(row):
            return Order(index+1,
                         row[Utilities.key_type],
                         row[Utilities.key_quantity],
                         row[Utilities.key_limit],
                         row[Utilities.key_price])
        return None

    @staticmethod
    def row_is_valid_buy_order(row):
        return (Utilities.key_exchange in row
                and Utilities.key_type
                and Utilities.key_quantity in row
                and Utilities.key_limit in row
                and Utilities.key_price in row
                and row[Utilities.key_type] == Utilities.LIMIT_BUY)
