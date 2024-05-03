""" Wrapper for Monnify Wallet API
The Wallet API allows you to create and manage digital wallets for customers
"""

from typing import Dict, Optional, Union
from monnifyease.core import MonnifyResponse, SyncRequestClient


class Wallet(SyncRequestClient):
    """Monnify Wallet API"""
    def create_wallet(
            self,
            wallet_ref: str,
            wallet_name: str,
            customer_name: str,
            customer_email: str,
            bvn_details: Dict[str, str]
    ) -> MonnifyResponse:
        """
        Creates wallet for customers
        Reference: https://developers.monnify.com/api/#Wallet-menu

        :param: wallet_ref:
        :param: wallet_name:
        :param: customer_name:
        :param: customer_email:
        :param: bvn_details:

        :return: The response from the API
        :rtype: MonnifyResponse object

        bvn_details = {
            "bvn": "123456789",
            "bvnDateOfBirth": "1993-04-23"
        }
        """

        data = {
            "walletReference": wallet_ref,
            "walletName": wallet_name,
            "customerName": customer_name,
            "customerEmail": customer_email,
            "bvnDetails": bvn_details,
        }

        return self._post("/v1/disbursements/wallet", data=data)

    def wallet_balance(self, wallet_ref: str) -> MonnifyResponse:
        """
        Gets the balance of the wallet
        :param: wallet_ref:

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        params = {"walletReference": wallet_ref}
        return self._get("v1/disbursements/wallet/balance", params=params)

    def get_wallets(
            self,
            customer_email: Optional[Union[str, None]] = None,
            per_page: Optional[Union[int, None]] = 0,
            page: Optional[Union[int, None]] = 50
    ) -> MonnifyResponse:
        """
        Gets all wallets
        :param: customer_email
        :param: per_page
        :param: page

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        params = {
            "customerEmail": customer_email,
            "pageSize": per_page,
            "pageNo": page
        }
        return self._get("/v1/disbursements/wallet", params=params)

    def get_wallet_transactions(
            self,
            account_number: Optional[Union[str, None]] = None,
            per_page: Optional[Union[int, None]] = 50,
            page: Optional[Union[int, None]] = 1
    ) -> MonnifyResponse:
        """
        Gets all wallet transactions
        :param: account_number
        :param: per_page
        :param: page

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        params = {
            "accountNumber": account_number,
            "pageSize": page,
            "pageNo": per_page
        }
        return self._get("/v1/disbursements/wallet/transactions", params=params)
