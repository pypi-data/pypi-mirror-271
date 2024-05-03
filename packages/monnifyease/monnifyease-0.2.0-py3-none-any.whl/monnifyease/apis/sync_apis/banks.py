""" Wrapper for Monnify Bank API
The Bank API allows you to get banks supported by Monnify
"""

from monnifyease.core import MonnifyResponse, SyncRequestClient


class Banks(SyncRequestClient):
    """Monnify Bank API"""
    def get_banks(self) -> MonnifyResponse:
        """
        Get all banks supported by Monnify
        Reference: https://developers.monnify.com/api/#get-banks

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        return self._get("/v1/banks")

    def get_bank_ussd_code(self) -> MonnifyResponse:
        """
        Get all banks with their USSD codes supported by Monnify

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        return self._get("/v1/sdk/transactions/banks")
