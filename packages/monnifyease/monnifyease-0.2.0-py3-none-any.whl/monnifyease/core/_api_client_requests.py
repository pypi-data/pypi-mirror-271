""" Implementation of the request methods """

from typing import Optional, Union, Dict, List, Any
from monnifyease.core._api_base_request import SyncBaseRequestClient
from monnifyease.core._api_client_response import MonnifyResponse


class SyncRequestClient(SyncBaseRequestClient):
    """Class representing a sync request client methods"""

    def _get(
        self,
        endpoint: str,
        params: Optional[Union[Dict[str, Any], List[Any], None]] = None,
        **kwargs,
    ) -> MonnifyResponse:
        """
        :param: endpoint
        :param: params
        :param: kwargs
        :return:
        """
        return self._request_url("GET", url=endpoint, params=params, **kwargs)

    def _post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Any], None]] = None,
        **kwargs,
    ) -> MonnifyResponse:
        """
        :param: endpoint
        :param: data
        :param: kwargs
        :return:
        """
        return self._request_url("POST", url=endpoint, data=data, **kwargs)

    def _put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Any], None]] = None,
        **kwargs,
    ) -> MonnifyResponse:
        """
        :param: endpoint
        :param: data
        :param: kwargs
        :return:
        """
        return self._request_url("PUT", url=endpoint, data=data, **kwargs)

    def _delete(self, endpoint: str, **kwargs) -> MonnifyResponse:
        """
        :param: endpoint
        :param: kwargs
        :return:
        """
        return self._request_url("DELETE", url=endpoint, **kwargs)
