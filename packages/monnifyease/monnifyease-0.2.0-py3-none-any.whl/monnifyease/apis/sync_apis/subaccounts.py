""" Wrapper for Monnify SubAccount API
The SubAccount API allows you to create and manage subaccounts for your customers so that transactions can be split
"""

from typing import Dict, List, Any
from monnifyease.core import MonnifyResponse, SyncRequestClient


class SubAccounts(SyncRequestClient):
    """ Monnify SubAccount API"""
    def create_sub_account(self, objects: List[Dict[str, Any]]) -> MonnifyResponse:
        """
        Creates a new SubAccount
        Reference: https://developers.monnify.com/api/#Sub%20Accounts-menu

        :param: objects:

        :return: The response form the API
        :rtype: MonnifyResponse object

        objects = [
            {
                "currencyCode": "NGN",
                "bankCode": "054",
                "accountNumber": "0809786785",
                "email": "tet123@gmail.com",
                "defaultSplitPercentage": 20.13
            }
        ]
        """

        return self._post("v1/sub-accounts", data=objects)

    def delete_sub_account(self, subaccount_code: str) -> MonnifyResponse:
        """
        Delete a Sub Account

        :param: subaccount_code:

        :return: The response form the API
        :rtype: MonnifyResponse object
        """
        return self._delete(f"v1/sub-accounts/{subaccount_code}")

    def get_sub_accounts(self) -> MonnifyResponse:
        """
        Get all Sub Accounts

        :return: The response form the API
        :rtype: MonnifyResponse object
        """
        return self._get("v1/sub-accounts/")

    def update_sub_accounts(
            self,
            subaccount_code: str,
            account_number: str,
            email: str,
            currency_code: str,
            bank_code: str,
            default_split_percentage: float
    ) -> MonnifyResponse:
        """
        Update a Sub Account\

        :param: subaccount_code:
        :param: account_number:
        :param: email:
        :param: currency_code:
        :param: bank_code:
        :param: default_split_percentage:

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "subAccountCode": subaccount_code,
            "accountNumber": account_number,
            "email": email,
            "currencyCode": currency_code,
            "bankCode": bank_code,
            "defaultSplitPercentage": default_split_percentage,
        }
        return self._put("v1/sub-accounts", data=data)
