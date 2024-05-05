"""
# Base Response

This module contains the base response class for the API.

## Classes:

* `BaseResponse`: A `TypedDict` that represents the structure of the base response
* `Error`: A `TypedDict` that represents the structure of the error
* `ErrorInformation`: A `TypedDict` that represents the structure of the error information
"""

from typing import Generic, TypedDict, TypeVar

__all__ = ["BaseResponse", "Error", "ErrorInformation"]

T = TypeVar("T")


class ErrorInformation(TypedDict):
    """
    Error Information.

    Attributes:
        reason (str): Reason.
        message (str): Message.

    Examples:
        >>> ErrorInformation(reason=..., message=...)
        {
            'reason': ...,
            'message': ...
        }
    """

    reason: str
    message: str


class Error(TypedDict):
    """
    Error.

    Attributes:
        message (str): Message.
        errors (list[ErrorInformation]): Errors.

    Examples:
        >>> Error(message=..., errors=...)
        {
            'message': ...,
            'errors': ...
        }
    """

    message: str
    errors: list[ErrorInformation] | None


class BaseResponse(TypedDict, Generic[T]):
    """
    Base Response.

    Attributes:
        data (T): Data.
        error (dict[str, str] | None): Error.
        status_code (int): Status code.
        success (bool): Success.

    Examples:
        >>> BaseResponse(data=..., error=..., status_code=..., success=...)
        {
            'data': ...,
            'error': ...,
            'status_code': ...,
            'success': ...
        }
    """

    data: T
    error: Error | None
    status_code: int
    success: bool
