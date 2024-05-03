""" Response object from Monnify API server """

from typing import Optional, Union, Dict, List, Any
from dataclasses import dataclass


@dataclass
class MonnifyResponse:
    """
    Monnify API Response from the server after HTTP requests have been made
    """

    status_code: int
    requestSuccessful: bool
    responseMessage: str
    responseCode: int
    responseBody: Optional[Union[Dict[str, Any], List[Any]]]

    @property
    def url(self) -> Optional[Union[str, None]]:
        """
        :return:
        """
        if (
            self.status_code == 200
            and self.responseBody
            and isinstance(self.responseBody, dict)
        ):
            return self.responseBody["checkoutUrl"]
        return None

    @property
    def transaction_reference(self) -> Optional[Union[str, None]]:
        """
        :return:
        """
        if (
            self.status_code == 200
            and self.responseBody
            and isinstance(self.responseBody, dict)
        ):
            return self.responseBody["transactionReference"]
        return None
