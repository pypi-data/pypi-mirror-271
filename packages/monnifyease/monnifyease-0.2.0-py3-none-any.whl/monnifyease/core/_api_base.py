"""
Base client API for Monnify API with methods for handling HTTP requests, authentication using a secret key,
constructing HTTP headers, joining URLs with the API base URL, and logging response information.
"""

import base64
import logging
from datetime import datetime, timedelta
from urllib.parse import urljoin

from requests import Session, RequestException

from monnifyease.core._api_base_envar import EnvBase
from monnifyease.core._api_errors import MonnifyEaseError


logger = logging.getLogger(__name__)


class MonnifyBaseClient:
    """Base Client API for Monnify API"""

    def __init__(self, env: EnvBase, session: Session = Session()) -> None:
        """
        Initialize the Monnify Base Client with the chosen environment

        :param: environment: the environment platform you want to connect

        :return: the connection to the server
        """
        self._env = env
        self._session = session
        self._access_token = None
        self._token_expiry = None

    def _generate_auth_basic(self) -> str:
        """
        Generates a Basic authentication header value by encoding the API key and secret key.

        Returns:
            str: The Basic authentication header value.
        """
        code = base64.b64encode(
            f"{self._env.get_api_key()}:{self._env.get_secret_key()}".encode()
        ).decode("utf-8")
        auth_code = f"Basic {code}"
        return auth_code

    def get_access_token(self) -> dict:
        """
        Retrieves a Monnify API access token.

        This method manages caching the access token and refreshes it before it expires.

        Returns:
            dict: A dictionary containing the authorization header, content type header,
                and user-agent header. The authorization header uses a Bearer token retrieved
                from the Monnify API.
        """
        if not self._access_token or datetime.now() > self._token_expiry:
            self._access_token = self._generate_access_token()
            self._token_expiry = datetime.now() + timedelta(
                seconds=self._access_token["responseBody"]["expiresIn"]
            )
        return {
            "Authorization": f"Bearer {self._access_token['responseBody']['accessToken']}",
            "Content-Type": "application/json",
            "User-Agent": "monnifyease/0.1.0",
        }

    def _generate_access_token(self) -> dict:
        """
        Generates a new Monnify API access token using Basic authentication.

        Returns:
            dict: A dictionary containing the access token, expiry time

        Raises:
            MonnifyEaseError: If there is an error during the access token request.
        """
        auth_code = self._generate_auth_basic()
        headers = {
            "Authorization": auth_code,
            "Content-Type": "application/json",
            "User-Agent": "monnifyease/0.1.0",
        }
        token_request_body = {"grant_type": "authorization_code"}

        try:
            access_response = self._session.post(
                url=urljoin(self._env.get_base_url(), "v1/auth/login"),
                headers=headers,
                json=token_request_body,
            )
            access_response.raise_for_status()
            access_token = access_response.json()
            return access_token
        except RequestException as error:
            error_message = str(error)
            status_code = getattr(error, "response", None) and getattr(
                error.response, "status_code", None
            )
            logger.error("Error %s:", error)
            raise MonnifyEaseError(
                message=error_message, status_code=status_code
            ) from error
