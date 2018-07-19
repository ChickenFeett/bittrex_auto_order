class Definition:
    #****************   I N P U T    F I L E   S T U F F   ****************
    # CSV Input file keys
    csv_key_order_uuid = "OrderUuid"
    csv_key_exchange = "Exchange"
    csv_key_type = "Type"
    csv_key_quantity = "Quantity"
    csv_key_limit = "Limit"
    csv_key_commission_paid = "CommissionPaid"
    csv_key_price = "Price"
    csv_key_opened = "Opened"
    csv_key_closed = "Closed"

    LIMIT_BUY = "LIMIT_BUY"
    LIMIT_SELL = "LIMIT_SELL"

    file_keys_historical_orders = [csv_key_order_uuid, csv_key_exchange, csv_key_type, csv_key_quantity, csv_key_limit, csv_key_commission_paid, csv_key_price, csv_key_opened, csv_key_closed]

    # Input json file keys
    file_key_crypto = "crypto"
    file_key_market = "market"
    file_key_quantity = "quantity"
    file_key_sell_quantity = "sell_quantity"
    file_key_buy_price = "buy_price"
    file_key_buy_cost = "buy_cost"
    file_key_sell_price = "sell_price"

    file_keys_orders = [file_key_crypto, file_key_market, file_key_quantity, file_key_sell_quantity, file_key_buy_price, file_key_buy_cost, file_key_sell_price]

    #****************   A P I   S T U F F   ****************

    api_key_message = "message"
    api_key_result = "result"

    # OPEN ORDERS keys
    api_key_OrderUuid = "OrderUuid"
    api_key_QuantityRemaining = "QuantityRemaining"
    api_key_IsConditional = "IsConditional"
    api_key_ImmediateOrCancel = "ImmediateOrCancel"
    api_key_Uuid = "Uuid"
    api_key_Exchange = "Exchange"
    api_key_OrderType = "OrderType"
    api_key_Price = "Price"
    api_key_CommissionPaid = "CommissionPaid"
    api_key_Opened = "Opened"
    api_key_Limit = "Limit"
    api_key_Closed = "Closed"
    api_key_ConditionTarget = "ConditionTarget"
    api_key_CancelInitiated = "CancelInitiated"
    api_key_PricePerUnit = "PricePerUnit"
    api_key_Condition = "Condition"
    api_key_Quantity = "Quantity"

    api_keys_open_orders = [api_key_OrderUuid, api_key_QuantityRemaining, api_key_IsConditional, api_key_ImmediateOrCancel, api_key_Uuid, api_key_Exchange, api_key_OrderType, api_key_Price, api_key_CommissionPaid, api_key_Opened, api_key_Limit, api_key_Closed, api_key_ConditionTarget, api_key_CancelInitiated, api_key_PricePerUnit, api_key_Condition, api_key_Quantity]

    # SUMMARY FOR MARKET
    api_key_MarketName = "MarketName"
    api_key_High = "High"
    api_key_Low = "Low"
    api_key_Volume = "Volume"
    api_key_Last = "Last"
    api_key_BaseVolume = "BaseVolume"
    api_key_TimeStamp = "TimeStamp"
    api_key_Bid = "Bid"
    api_key_Ask = "Ask"
    api_key_OpenBuyOrders = "OpenBuyOrders"
    api_key_OpenSellOrders = "OpenSellOrders"
    api_key_PrevDay = "PrevDay"
    api_key_Created = "Created"

    api_keys_market_summary = [api_key_MarketName, api_key_High, api_key_Low, api_key_Volume, api_key_Last, api_key_BaseVolume, api_key_TimeStamp, api_key_Bid, api_key_Ask, api_key_OpenBuyOrders, api_key_OpenSellOrders, api_key_PrevDay, api_key_Created]

    # BALANCES
    api_key_Currency = "Currency"
    api_key_Balance = "Balance"
    api_key_Available = "Available"
    api_key_Pending = "Pending"
    api_key_CryptoAddress = "CryptoAddress"

    api_keys_balance = [api_key_Currency, api_key_Balance, api_key_Available, api_key_Pending, api_key_CryptoAddress]


    def __init__(self):
        pass