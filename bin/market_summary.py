class MarketSummary:
    market_name = None
    high = None
    low = None
    volume = None
    last = None
    base_volume = None
    timestamp = None
    bid = None
    ask = None
    open_buy_orders = None
    open_sell_orders = None
    prev_day = None
    created = None

    def __init__(self, market_name, high, low, volume, last, base_volume, timestamp, bid, ask, open_buy_orders, open_sell_orders, prev_day, created):
        self.market_name = market_name
        self.high = float(high)
        self.low = float(low)
        self.volume = volume
        self.last = last
        self.base_volume = base_volume
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.open_buy_orders = open_buy_orders
        self.open_sell_orders = open_sell_orders
        self.prev_day = prev_day
        self.created = created
        if (self.market_name is None or
            self.high is None or
            self.low is None or
            self.volume is None or
            self.last is None or
            self.base_volume is None or
            self.timestamp is None or
            self.bid is None or
            self.ask is None or
            self.open_buy_orders is None or
            self.open_sell_orders is None or
            self.prev_day is None or
            self.created is None):
            raise ValueError("MarketSummary initialized with invalid value")
