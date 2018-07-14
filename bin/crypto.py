class Crypto:
    order_id = 0
    crypto_type = ''
    quantity = 0.0
    buy_price = 0.0
    buy_cost = 0.0

    def __init__(self, order_id, crypto_type, quantity, buy_price, buy_cost):
        self.order_id = int(order_id)
        self.crypto_type = str(crypto_type)
        self.quantity = float(quantity)
        self.buy_price = float(buy_price)
        self.buy_cost = float(buy_cost)
