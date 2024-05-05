import hashlib
from deropy.dvm.Smartcontract import SmartContract


class Wallet:
    def __init__(self, id):
        self.id = id
        self.string_address = hashlib.sha256(str(id).encode()).hexdigest()
        self.raw_address = self.string_address[:33]
        self.balance = {}

    @classmethod
    def from_public_key(cls, public_key):
        wallet = cls(public_key)
        wallet.string_address = public_key
        wallet.raw_address = public_key[:33]
        return wallet

    def invoke_sc_function(self, func, func_args: tuple = None, dero_deposit: int = None, asset_deposit: tuple = None):
        WalletSimulator.active_wallet = self.id

        if dero_deposit is not None:
            SmartContract.send_dero_with_tx(dero_deposit)
        if asset_deposit is not None:
            SmartContract.send_asset_with_tx(asset_deposit[0], asset_deposit[1])

        if func_args is None:
            return func()

        if not isinstance(func_args, (tuple, list)):
            func_args = (func_args,)

        return func(*func_args)

    def get_balance(self, token):
        return self.balance.get(token, 0)

    def set_balance(self, token, amount):
        self.balance[token] = amount


class WalletSimulator:
    active_wallet = None
    wallets = {}

    @staticmethod
    def create_wallet(id):
        WalletSimulator.wallets[id] = Wallet(id)
        return WalletSimulator.wallets[id]

    @staticmethod
    def create_wallet_from_public_key(id, public_key):
        WalletSimulator.wallets[id] = Wallet.from_public_key(public_key)

    @staticmethod
    def find_wallet_id_from_string(string_address):
        for id, wallet in WalletSimulator.wallets.items():
            if wallet.string_address == string_address:
                return id
        raise Exception("Wallet not found")

    @staticmethod
    def find_wallet_id_from_raw(raw_address):
        for id, wallet in WalletSimulator.wallets.items():
            if wallet.raw_address == raw_address:
                return id
        raise Exception("Wallet not found")
    
    @staticmethod
    def get_wallet_from_raw(raw_address):
        id = WalletSimulator.find_wallet_id_from_raw(raw_address)
        return WalletSimulator.get_wallet_from_id(id)
    
    @staticmethod
    def get_wallet_from_id(id):
        return WalletSimulator.wallets[id]

    @staticmethod
    def get_raw_address():
        return WalletSimulator.wallets[WalletSimulator.active_wallet].raw_address

    @staticmethod
    def get_string_address():
        return WalletSimulator.wallets[WalletSimulator.active_wallet].string_address

    @staticmethod
    def get_raw_address_from_id(id):
        return WalletSimulator.wallets[id].raw_address

    def get_string_address_from_id(id):
        return WalletSimulator.wallets[id].string_address

    @staticmethod
    def is_initialized():
        return WalletSimulator.active_wallet is not None
