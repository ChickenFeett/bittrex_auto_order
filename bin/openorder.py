class OpenOrder:
    order_uuid = None
    quantity_remaining = None
    is_conditional = None
    immediate_or_cancel = None
    uuid = None
    exchange = None
    order_type = None
    price = None
    commission_paid = None
    opened = None
    limit = None
    closed = None
    condition_target = None
    cancel_initiated = None
    price_per_unit = None
    condition = None
    quantity = None

    def __init__(self, order_uuid, quantity_remaining, is_conditional, immediate_or_cancel, uuid, exchange, order_type, price, commission_paid, opened, limit, closed, condition_target, cancel_initiated, price_per_unit, condition, quantity):
        self.order_uuid = str(order_uuid)
        self.quantity_remaining = float(quantity_remaining)
        self.is_conditional = str(is_conditional)
        self.immediate_or_cancel = str(immediate_or_cancel)
        self.uuid = str(uuid)
        self.exchange = str(exchange)
        self.order_type = str(order_type)
        self.price = float(price)
        self.commission_paid = float(commission_paid)
        self.opened = str(opened)
        self.limit = float(limit)
        self.closed = str(closed)
        self.condition_target = str(condition_target)
        self.cancel_initiated = str(cancel_initiated)
        self.price_per_unit = str(price_per_unit)
        self.condition = str(condition)
        self.quantity = float(quantity)
        if (self.order_uuid is None or
           self.quantity_remaining is None or
           self.is_conditional is None or
           self.immediate_or_cancel is None or
           self.uuid is None or
           self.exchange is None or
           self.order_type is None or
           self.price is None or
           self.commission_paid is None or
           self.opened is None or
           self.limit is None or
           self.closed is None or
           self.condition_target is None or
           self.cancel_initiated is None or
           self.price_per_unit is None or
           self.condition is None or
           self.quantity is None):
            raise ValueError("Crypto initialized with invalid value")
