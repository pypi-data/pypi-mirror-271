""" Wrapper classes for various Synchronous Monnify API endpoints,
providing simplified access to functionality in Monnify
"""

from monnifyease.apis import (
    banks,
    customer_reserved_account,
    settlements,
    subaccounts,
    transactions,
    wallet
)


class Monnify:
    """Monnify acts as a wrapper around various client APIs to
    interact with the Monnify API
    """
    def __init__(self) -> None:
        self.banks = banks.Banks()
        self.reserve_account = customer_reserved_account.CustomerReservedAccount()
        self.settlements = settlements.Settlements()
        self.subaccounts = subaccounts.SubAccounts()
        self.transactions = transactions.Transactions()
        self.wallet = wallet.Wallet()
