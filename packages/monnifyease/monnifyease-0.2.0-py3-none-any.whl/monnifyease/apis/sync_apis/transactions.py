""" Wrapper for Monnify Transactions API
The Transactions API allows you to create and manage payments on your integration.
"""

from datetime import date
from typing import Optional, List, Dict, Any, Union

from monnifyease.core import MonnifyResponse, SyncRequestClient
from monnifyease.helpers.tool_kit import PaymentMethods, Currency
from monnifyease.utils.convert_to_strings import convert_to_string


class Transactions(SyncRequestClient):
    """Monnify Transaction API"""

    def initialize_transaction(
            self,
            amount: float,
            customer_name: str,
            customer_email: str,
            payment_reference: str,
            payment_description: str,
            currency: Currency,
            merchant_code: str,
            payment_methods: Optional[Union[List[PaymentMethods], None]] = None,
            redirect_url: Optional[Union[str, None]] = None,
            income_split_config: Optional[Union[List[Dict[str, Any]], None]] = None,
            metadata: Optional[Union[Dict[str, Any], None]] = None,
    ) -> MonnifyResponse:
        """
        Create a transaction
        Reference: https://developers.monnify.com/api/#initialize-transaction

        :param: amount
        :param: customer_name
        :param: customer_email
        :param: payment_reference: A unique string of characters that identifies each transaction
        :param: payment_description: Reason of payment
        :param: currency
        :param: merchant_code: The merchant contract code
        :param: redirect_url: A url to redirect to after payment completion
        :param: payment_methods: The method of payment collection
        :param: income_split_config: A way to split payments among subAccounts.
        :param: metadata: pass extra information from customers.

        :return: The response form the API
        :rtype: MonnifyResponse object
        """
        data = {
            "amount": amount,
            "customerName": customer_name,
            "customerEmail": customer_email,
            "paymentReference": payment_reference,
            "paymentDescription": payment_description,
            "currencyCode": currency,
            "contractCode": merchant_code,
            "redirectUrl": redirect_url,
            "paymentMethods": payment_methods,
            "incomeSplitConfig": income_split_config,
            "metadata": metadata,
        }
        return self._post("/v1/merchant/transactions/init-transaction", data=data)

    def pay_with_bank_transfer(
            self, transaction_reference: str, bank_code: str
    ) -> MonnifyResponse:
        """
        Create a transaction
        Reference: https://developers.monnify.com/api/#initialize-transaction

        :param: transaction_reference: This is the transaction reference gotten from the initialize_transaction method
        :param: bank_code

        :return: The response form the API
        :rtype: MonnifyResponse object
        """
        data = {"transactionReference": transaction_reference, "bankCode": bank_code}
        return self._post("/v1/merchant/bank-transfer/init-payment", data=data)

    def charge_card(
            self,
            transaction_reference: str,
            card: Dict[str, str],
            collection_channel: Optional[str] = "API_NOTIFICATION",
    ) -> MonnifyResponse:
        """
        Initiate a charge on a card
        Reference: https://developers.monnify.com/api/#charge-card

        :param: transaction_reference
        :param: collection_channel
        :param: card: The card to charge

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "transactionReference": transaction_reference,
            "collectionChannel": collection_channel,
            "card": card,
        }
        return self._post("/v1/merchant/cards/charge", data=data)

    def authorize_otp(
            self,
            transaction_reference: str,
            token_id: str,
            token: str,
            collection_channel: Optional[str] = "API_NOTIFICATION",
    ) -> MonnifyResponse:
        """
        Authorize an OTP to complete a charge on a card
        Reference: https://developers.monnify.com/api/#authorize-otp

        :param: transaction_reference
        :param: collection_channel
        :param: token_id
        :param: token

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "transactionReference": transaction_reference,
            "collectionChannel": collection_channel,
            "tokenId": token_id,
            "token": token,
        }
        return self._post("/v1/merchant/cards/charge", data=data)

    def authorize_3ds(
            self,
            transaction_reference: str,
            card: Dict[str, str],
            collection_channel: Optional[str] = "API_NOTIFICATION",
            api_key: Optional[Union[str, None]] = None,
    ) -> MonnifyResponse:
        """
        Authorizes charge on a card that uses 3DS Secure Authentication.
        Reference: https://developers.monnify.com/api/#authorize-3ds-card

        :param: transaction_reference
        :param: collection_channel
        :param: card
        :param: api_key

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "transactionReference": transaction_reference,
            "collectionChannel": collection_channel,
            "card": card,
            "apiKey": api_key,
        }
        return self._post("v1/sdk/cards/secure-3d/authorize", data=data)

    def list_transaction(
            self,
            per_page: Optional[Union[int, None]] = 0,
            page_size: Optional[Union[int, None]] = 50,
            payment_reference: Optional[Union[str, None]] = None,
            transaction_reference: Optional[Union[str, None]] = None,
            from_amount: Optional[Union[float, None]] = None,
            to_amount: Optional[Union[float, None]] = None,
            amount: Optional[Union[float, None]] = None,
            customer_name: Optional[Union[str, None]] = None,
            customer_email: Optional[Union[str, None]] = None,
            payment_status: Optional[Union[str, None]] = None,
            from_date: Optional[Union[date, None]] = None,
            to_date: Optional[Union[date, None]] = None,
    ) -> MonnifyResponse:
        """
        Get all Transactions List
        Reference: https://developers.monnify.com/api/#get-all-transactions

        :param: per_page
        :param: page_size
        :param: payment_reference
        :param: transaction_reference
        :param: from_amount
        :param: to_amount
        :param: amount
        :param: customer_name
        :param: customer_email
        :param: payment_status
        :param: from_date
        :param: to_date

        :return: The response form the API
        :rtype: MonnifyResponse object
        """

        # convert to string
        from_date = convert_to_string(from_date)
        to_date = convert_to_string(to_date)

        params = {
            "page": per_page,
            "size": page_size,
            "paymentReference": payment_reference,
            "transactionReference": transaction_reference,
            "fromAmount": from_amount,
            "toAmount": to_amount,
            "amount": amount,
            "customerName": customer_name,
            "customerEmail": customer_email,
            "paymentStatus": payment_status,
            "from": from_date,
            "to": to_date,
        }
        return self._get("/v1/transactions/search", params=params)

    def get_transaction_status(self, transaction_reference: str) -> MonnifyResponse:
        """
        Status of a transaction
        Reference: https://developers.monnify.com/api/#get-transaction-status

        :param: transaction_reference

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        # params = {"transactionReference": transaction_reference}
        return self._get(f"/v2/transactions/{transaction_reference}")
