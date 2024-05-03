""" Environment variables for the application to be executed when the application is started"""

from typing import Protocol
from decouple import config
from monnifyease.core._api_errors import EnvKeyError


MERCHANT_CODE = config("MONNIFY_CONTRACT_CODE")


class EnvBase(Protocol):
    """
    This is a base protocol that defines the methods required to access environment variables
    used by the MonnifyEase library.

    Implementations of this protocol should provide concrete methods for retrieving the environment variables:
        - MONNIFY_API_KEY: The Monnify API key used for authentication.
        - MONNIFY_SECRET_KEY: The Monnify secret key used for authentication.
        - MONNIFY_BASE_URL: The base URL of the Monnify API.
    """

    def get_api_key(self) -> str:
        """
        Retrieves the Monnify API key from environment variables.

        Raises:
            EnvKeyError: If the MONNIFY_API_KEY environment variable is not set.

        Returns:
            str: The Monnify API key.
        """

    def get_secret_key(self) -> str:
        """
        Retrieves the Monnify SECRET key from environment variables.

        Raises:
            EnvKeyError: If the MONNIFY_SECRET_KEY environment variable is not set.

        Returns:
            str: The Monnify SECRET key.
        """

    def get_base_url(self) -> str:
        """
        Retrieves the Monnify BASE URL from environment variables.

        Raises:
            EnvKeyError: If the MONNIFY_BASE_URL environment variable is not set.

        Returns:
            str: The Monnify BASE URL.
        """


class EnvConfig(EnvBase):
    """The configuration"""
    @classmethod
    def get_api_key(cls):
        """
        See EnvBase.get_api_key()
        """
        api_key = config("MONNIFY_API_KEY")
        if not api_key:
            raise EnvKeyError(
                message="Kindly ensure you have MONNIFY_API_KEY variable intact"
            )
        return api_key

    @classmethod
    def get_secret_key(cls):
        """
        See EnvBase.get_secret_key()
        """
        secret_key = config("MONNIFY_SECRET_KEY")
        if not secret_key:
            raise EnvKeyError(
                message="Kindly ensure you have MONNIFY_SECRET_KEY variable intact"
            )
        return secret_key

    @classmethod
    def get_base_url(cls):
        """
        See EnvBase.get_base_url()
        """
        base_url = config("MONNIFY_BASE_URL")
        if not base_url:
            raise EnvKeyError(
                message="Kindly ensure you have MONNIFY_BASE_URL variable intact"
            )
        return base_url
