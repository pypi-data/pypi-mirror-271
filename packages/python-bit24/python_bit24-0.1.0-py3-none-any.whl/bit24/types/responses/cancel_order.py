"""
# Cancel Order Response

This module contains the response class for the Cancel Order API.

## Classes:

* `CancelOrderResponse`: A `TypedDict` that represents the structure of the cancel order response
"""

from typing import TypedDict

__all__ = ["CancelOrderResponse"]


class CancelOrderResponse(TypedDict):
    """
    Cancel Order Response.

    Attributes:
        message (str): Message.

    Examples:
        >>> CancelOrderResponse(message="message")
        {'message': 'message'}
    """

    message: str
