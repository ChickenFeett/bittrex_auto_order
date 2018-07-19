class Order:
    order_id = None
    crypto = None
    market = None
    quantity = None
    sell_quantity = None
    buy_price = None
    buy_cost = None
    sell_price = None

    def __init__(self, order_id, crypto, market, quantity, sell_quantity, buy_price, buy_cost, sell_price):
        self.order_id = int(order_id)
        self.crypto = str(crypto)
        self.market = str(market)
        self.quantity = float(quantity)
        self.sell_quantity = float(sell_quantity)
        self.buy_price = float(buy_price)
        self.buy_cost = float(buy_cost)
        self.sell_price = float(sell_price)
        if (self.order_id is None or
            self.crypto is None or
            self.market is None or
            self.quantity is None or
            self.sell_quantity is None or
            self.buy_price is None or
            self.buy_cost is None or
            self.sell_price is None):
            raise ValueError("Order initialized with invalid value")