"""Enums classes with predefined values."""

from enum import Enum


class Currency(Enum):
    """Currencies supported by Monnify."""

    NGN = "NGN"
    USD = "USD"


class PaymentMethods(Enum):
    """Channels supported by Monnify."""

    ACCOUNT_TRANSFER = "ACCOUNT_TRANSFER"
    CARD = "CARD"
    PHONE_NUMBER = "PHONE_NUMBER"
    USSD = "USSD"
