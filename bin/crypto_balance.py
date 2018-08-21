class CryptoBalance:
    crypo_balance_id = None
    currency = None
    balance = None
    available = None
    pending = None
    crypto_address = None

    def __init__(self, crypo_balance_id, currency, balance, available, pending, crypto_address):
        self.number = int(crypo_balance_id)
        self.crypo_balance_id = int(crypo_balance_id)
        self.currency = str(currency)
        self.balance = float(balance)
        self.available = float(available)
        self.pending = float(pending)
        self.crypto_address = str(crypto_address)
        if (self.number is None or
            self.crypo_balance_id is None or
            self.currency is None or
            self.balance is None or
            self.available is None or
            self.pending is None or
            self.crypto_address is None):
            raise ValueError("Crypto initialized with invalid value")
