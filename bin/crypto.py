class Crypto:
    order_id = 0
    crypto_type = ''
    quantity = 0
    buy_price = 0
    buy_cost = 0

    def __init__(self, order_id, crypto_type, quantity, buy_price, buy_cost):
        self.order_id = str(order_id)
        self.crypto_type = str(crypto_type)
        self.quantity = str(quantity)
        self.buy_price = str(buy_price)
        self.buy_cost = str(buy_cost)
