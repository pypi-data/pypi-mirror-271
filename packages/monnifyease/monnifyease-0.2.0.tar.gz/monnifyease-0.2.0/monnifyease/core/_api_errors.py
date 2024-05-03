""" MonnifyEase Error Message"""


class MonnifyEaseError(Exception):
    """
    Base exception class for Monnify API errors
    """

    def __init__(self, message: str, status_code: int = None) -> None:
        self.message = message
        self.status_code = status_code
        super(MonnifyEaseError, self).__init__(
            f"\nError Message: {self.message}\nError Status Code: {self.status_code}"
        )


class EnvKeyError(MonnifyEaseError):
    """
    Secret Key Error
    """

    def __init__(self, message: str, status_code: int = 401) -> None:
        super().__init__(message, status_code)


class TypeValueError(MonnifyEaseError):
    """
    Type Value Error
    """

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message, status_code)


class InvalidRequestMethodError(MonnifyEaseError):
    """
    Request Time Error
    """

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message, status_code)
