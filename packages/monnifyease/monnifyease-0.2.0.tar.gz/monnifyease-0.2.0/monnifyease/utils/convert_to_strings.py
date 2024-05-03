""" Implements the conversion of data types to strings """

import logging
from typing import Union
from datetime import date, datetime

from monnifyease.core._api_errors import TypeValueError


logger = logging.getLogger(__name__)


def convert_to_string(value: Union[bool, date, datetime, None]) -> Union[str, int, None]:
    """
    Convert the type of value to a string
    :param value: The value to be converted

    :raise TypeError: if the value is not a supported type

    :return: The value as a string
    :rtype: str
    """
    # each supported type is mapped to its corresponding conversion function
    conversion_functions = {
        bool: str,
        date: lambda val: val.strftime("%Y-%m-%d"),
        datetime: lambda val: val.strftime("%Y-%m-%d %H:%M:%S"),
    }

    if value is None:
        return None
    if type(value) in conversion_functions:
        return conversion_functions[type(value)](value)
    error_message = f"Unsupported type: {type(value)}. Expected type -bool, -date"
    logger.error("Unsupported type: %s Expected type -bool, -date", {type(value)})
    raise TypeValueError(error_message)
