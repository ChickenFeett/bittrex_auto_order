class OpenOrder:
    number = 0
    market = ''
    quantity = 0.0
    buy_price = 0.0
    buy_cost = 0.0

    def __init__(self, number, market, quantity, buy_price, buy_cost):
        self.number = int(number)
        self.market = str(market)
        self.quantity = float(quantity)
        self.buy_price = float(buy_price)
        self.buy_cost = float(buy_cost)
        if (self.number is None or
            self.market is None or
            self.quantity is None or
            self.buy_price is None or
            self.buy_cost  is None):
            raise ValueError("Crypto initialized with invalid value")
