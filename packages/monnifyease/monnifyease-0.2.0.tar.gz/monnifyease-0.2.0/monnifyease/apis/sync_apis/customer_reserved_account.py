""" Wrapper for Monnify Customer Reserved Account API
The Customer API allows you to create and manage payments on your integration.
"""

from typing import List, Dict, Any, Optional, Union
from monnifyease.core import MonnifyResponse, SyncRequestClient
from monnifyease.helpers.tool_kit import Currency


class CustomerReservedAccount(SyncRequestClient):
    """Monnify Customer Reserved Account API"""

    def create_general_reserve(
            self,
            account_reference: str,
            account_name: str,
            currency: Currency,
            merchant_code: str,
            customer_email: str,
            customer_name: str,
            bvn: str,
            nin: str,
            income_split_config: Optional[List[Dict[str, Any]]] = None,
            allow_pay_source: Optional[Dict[str, List[Any]]] = None,
            restrict_pay_source: Optional[bool] = False,
            preferred_bank: Optional[Union[List[Any], None]] = None,
            get_all_banks: Optional[bool] = True,
    ) -> MonnifyResponse:
        """
        Creation of dedicated virtual accounts for your customers (General).
        Reference: https://developers.monnify.com/api/#create-reserved-accountgeneral

        :param: account_reference
        :param: account_name
        :param: currency
        :param: merchant_code
        :param: customer_email
        :param: customer_name
        :param: bvn
        :param: nin
        :param: preferred_bank
        :param: income_split_config
        :param: allow_pay_source
        :param: restrict_pay_source
        :param: get_all_banks

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "accountReference": account_reference,
            "accountName": account_name,
            "currencyCode": currency,
            "contractCode": merchant_code,
            "customerEmail": customer_email,
            "customerName": customer_name,
            "bvn": bvn,
            "nin": nin,
            "preferredBanks": preferred_bank,
            "incomeSplitConfig": income_split_config,
            "allowedPaymentSource": allow_pay_source,
            "restrictPaymentSource": restrict_pay_source,
            "getAllAvailableBanks": get_all_banks,
        }
        return self._post("/v2/bank-transfer/reserved-accounts", data=data)

    def create_invoice_reserve(
            self,
            account_reference: str,
            account_name: str,
            currency: str,
            merchant_code: str,
            customer_email: str,
            customer_name: str,
            bvn: str,
            nin: str,
            reserved_account: Optional[str] = "INVOICE",
    ) -> MonnifyResponse:
        """
         Creation of an invoiced reserved account.
        Reference: https://developers.monnify.com/api/#create-reserved-accountinvoice

        :param: account_reference
        :param: account_name
        :param: currency
        :param: merchant_code
        :param: customer_email
        :param: customer_name
        :param: reserved_account
        :param: bvn
        :param: nin

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "accountReference": account_reference,
            "accountName": account_name,
            "currencyCode": currency,
            "contractCode": merchant_code,
            "customerEmail": customer_email,
            "customerName": customer_name,
            "reservedAccountType": reserved_account,
            "bvn": bvn,
            "nin": nin,
        }
        return self._post("/v1/bank-transfer/reserved-accounts", data=data)

    def get_reserve_detail(self, account_reference: str) -> MonnifyResponse:
        """
        Get details of a reserved account.
        Reference: https://developers.monnify.com/api/#get-reserved-account-details

        :param: account_reference

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        return self._get(f"/v2/bank-transfer/reserved-accounts/{account_reference}")

    def add_linked_account(
            self,
            account_reference: str,
            preferred_bank: Optional[Union[List[str], None]] = None,
            get_all_banks: Optional[bool] = True
    ) -> MonnifyResponse:
        """
        Add a linked account to a reserved account.
        Reference: https://developers.monnify.com/api/#add-linked-accounts

        :param: preferred_bank
        :param: account_reference
        :param: get_all_banks

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "preferredBank": preferred_bank,
            "getAllAvailableBanks": get_all_banks,
        }
        return self._put(
            f"v1/bank-transfer/reserved-accounts/add-linked-accounts/{account_reference}",
            data=data,
        )

    def update_bvn_reserve(self, account_reference: str, bvn: str) -> MonnifyResponse:
        """
        Update the BVN of a reserved account.
        Reference: https://developers.monnify.com/api/#update-bvn-for-a-reserve-account

        :param: bvn
        :param: account_reference

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "bvn": bvn,
        }
        return self._put(
            f"/v1/bank-transfer/reserved-accounts/update-customer-bvn/{account_reference}",
            data=data,
        )

    def allow_payment_source(
            self,
            account_reference: str,
            allow_payment_source: Dict[str, List[Any]],
            restrict_pay_source: Optional[bool] = True,
    ) -> MonnifyResponse:
        """
        Manages accounts of a reserved account using [BVNs, Account Name or Account Number].
        Reference: https://developers.monnify.com/api/#allowed-payment-sources

        :param: allow_payment_source
        :param: account_reference
        :param: payment_source

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "allowedPaymentSource": allow_payment_source,
            "restrictPaymentSource": restrict_pay_source,
        }
        return self._put(
            f"/v1/bank-transfer/reserved-accounts/update-payment-source-filter/{account_reference}",
            data=data,
        )

    def update_split_config_account(
            self,
            account_reference: str,
            objects: List[Dict[str, Any]]
    ) -> MonnifyResponse:
        """
        Updates the split config of a customer reserved account.
        Reference: https://developers.monnify.com/api/#updating-split-config-for-reserved-account

        :param: account_reference
        :param: objects contains list of dictionaries.
        [
            {
                "subAccountCode": {{SubaccountCode}},
                "feePercentage": {{fee in percent}},
                "splitPercentage": {{split in percent}},
                "feeBearer": {{true or false}}
            }
        ]

        :return: Response from the API
        :rtype: MonnifyResponse object
        """
        return self._put(
            f"/v1/bank-transfer/reserved-accounts/update-income-split-config/{account_reference}",
            data=objects,
        )

    def deallocate_customer(self, account_reference: str) -> MonnifyResponse:
        """
        Deallocate/delete already created a reserved account.
        Reference: https://developers.monnify.com/api/#deallocating-a-reserved-account

        :param: account_reference

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        return self._delete(f"/v1/bank-transfer/reserved-accounts/{account_reference}")

    def get_reserve_transactions(
        self, account_reference: str, per_page: Optional[Union[int, None]] = 50, page: Optional[Union[int, None]] = 0
    ) -> MonnifyResponse:
        """
        Get transactions for a reserved account.
        Reference: https://developers.monnify.com/api/#get-transactions-for-a-reserved-account

        :param: account_reference
        :param: per_page
        :param: page

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        params = {"accountReference": account_reference, "page": page, "size": per_page}
        return self._get(
            "/v1/bank-transfer/reserved-accounts/transactions", params=params
        )

    def update_kyc_info(
            self, account_reference: str, bvn: str, nin: str
    ) -> MonnifyResponse:
        """
        This links customers' BVN/NIN to their respective reserved accounts.
        Reference: https://developers.monnify.com/api/#update-kyc-info

        :param: account_reference
        :param: bvn
        :param: nin

        :return: The response from the API
        :rtype: MonnifyResponse object
        """
        data = {
            "bvn": bvn,
            "nin": nin,
        }
        return self._put(
            f"/v1/bank-transfer/reserved-accounts/{account_reference}/kyc-info",
            data=data,
        )
