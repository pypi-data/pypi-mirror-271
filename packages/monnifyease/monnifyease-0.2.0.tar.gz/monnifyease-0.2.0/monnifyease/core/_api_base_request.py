""" Base class for implementing requests"""

import json
import logging
from typing import Optional, Union, Any, List, Dict

from requests import RequestException, Session

from monnifyease.core._api_access_header import AccessHeader
from monnifyease.core._api_client_response import MonnifyResponse
from monnifyease.core._api_errors import MonnifyEaseError, InvalidRequestMethodError
from monnifyease.utils.join_url import join_url


logger = logging.getLogger(__name__)


class SyncBaseRequestClient:
    """Monnify Request"""

    _VALID_HTTP_METHODS: set[str] = {"GET", "POST", "PUT", "DELETE"}

    def __init__(
        self, session: Session = Session(), auth_header: AccessHeader = AccessHeader()
    ) -> None:
        """Monnify Request"""
        self._session = session
        self._access_header = auth_header

    def _request_url(
        self,
        method: str,
        url: str,
        data: Optional[Union[Dict[str, Any], List[Any], None]] = None,
        params: Optional[Union[Dict[str, Any], List[Any], None]] = None,
        **kwargs,
    ) -> MonnifyResponse:
        """
        :param method:
        :param url:
        :param data:
        :param params:
        :param kwargs:
        :return:
        """
        if method.upper() not in self._VALID_HTTP_METHODS:
            error_message = f"Invalid HTTP method. Supported methods are GET, POST, PUT, DELETE. {method}"
            logger.error(error_message)
            raise InvalidRequestMethodError(error_message)

        url = join_url(url)

        # Filtering params and data, then converting data to JSON
        params = (
            {key: value for key, value in params.items() if value is not None}
            if params
            else None
        )
        data = json.dumps(data) if data else None
        try:
            with self._session.request(
                method=method,
                headers=self._access_header.get_auth_header(),
                url=url,
                data=data,
                params=params,
                **kwargs,
                timeout=10,
            ) as response:
                logger.info("Response Status Code: %s", response.status_code)
                logger.info("Response JSON: %s", response.json())
                response_data = response.json()
                return MonnifyResponse(
                    status_code=response.status_code,
                    requestSuccessful=response_data.get("requestSuccessful"),
                    responseMessage=response_data.get("responseMessage"),
                    responseCode=response_data.get("responseCode"),
                    responseBody=response_data.get("responseBody"),
                )
        except RequestException as error:
            error_message = str(error)
            status_code = getattr(error, "response", None) and getattr(
                error.response, "status_code", None
            )
            logger.error("Error %s:", error)
            raise MonnifyEaseError(
                message=error_message, status_code=status_code
            ) from error
