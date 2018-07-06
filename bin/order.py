class Order:
    order_id = 0
    crypto_type = ''
    quantity = 0
    buy_price = 0
    buy_cost = 0

    def __init__(self, order_id, crypto_type, quantity, buy_price, buy_cost):
        self.order_id = order_id
        self.crypto_type = crypto_type
        self.quantity = quantity
        self.buy_price = buy_price
        self.buy_cost = buy_cost
