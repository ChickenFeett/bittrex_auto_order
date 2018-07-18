class Order:
    order_id = 0
    market = ''
    quantity = 0.0
    buy_price = 0.0
    buy_cost = 0.0

    def __init__(self, order_id, market, quantity, buy_price, buy_cost):
        self.order_id = int(order_id)
        self.market = str(market)
        self.quantity = float(quantity)
        self.buy_price = float(buy_price)
        self.buy_cost = float(buy_cost)
        self.sell_price = self.buy_price * 2
        self.sell_total = self.sell_price * self.quantity
        if (self.order_id is None or
            self.market is None or
            self.quantity is None or
            self.buy_price is None or
            self.buy_cost is None or
            self.sell_price is None or
            self.sell_total is None):
            raise ValueError("Order initialized with invalid value")
