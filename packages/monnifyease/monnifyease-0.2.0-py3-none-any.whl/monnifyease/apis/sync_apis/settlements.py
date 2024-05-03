""" Wrapper for Monnify Settlement API
The Settlement API credits your wallet or bank account for payments made by your customers
"""

from monnifyease.core import MonnifyResponse, SyncRequestClient


class Settlements(SyncRequestClient):
    """Monnify Settlement API"""
    def get_transaction_settlement(
            self,
            reference: str,
            per_page: int,
            page: int
    ) -> MonnifyResponse:
        """
        Get transactions that are made up by settlement
        Reference: https://developers.monnify.com/api/#Settlements-menu

        :param: reference:
        :param: per_page:
        :param: page:

        :return: The response from the API
        :rtype: MonnifyResponse object
        """

        params = {"reference": reference, "page": per_page, "size": page}
        return self._get("/v1/transactions/find-by-settlement-reference", params=params)

    def get_transaction_settlement_info(self, transaction_reference: str) -> MonnifyResponse:
        """
        Get transaction settlement information for a given transaction
        :param: transaction_reference:

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        params = {"transactionReference": transaction_reference}
        return self._get("/v1/settlement-detail", params=params)
