""" This implements joining the base url with the given path"""

from urllib.parse import urljoin
from monnifyease.core._api_base_envar import EnvConfig, EnvBase


def join_url(path: str, env: EnvBase = EnvConfig()) -> str:
    """
    Join URL with Paystack API URL
    :param env:
    :param path:
    :return:
    """
    base_url = env.get_base_url()
    if path.startswith("/"):
        path = path[1:]
    return urljoin(base_url, path)
