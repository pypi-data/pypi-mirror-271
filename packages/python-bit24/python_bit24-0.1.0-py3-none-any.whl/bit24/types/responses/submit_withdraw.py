"""
# Submit Withdraw Response

This module contains the type definitions for the response of the submit withdraw endpoint.

## Classes

* `SubmitWithdrawResponse`: A `TypedDict` that represents the structure of the submit withdraw response.
"""

from typing import TypedDict

__all__ = ["SubmitWithdrawResponse"]


class SubmitWithdrawResponse(TypedDict):
    """
    Submit Withdraw Response.

    Attributes:
        message (str): Message.

    Examples:
        >>> SubmitWithdrawResponse(message="message")
        {
            'message': 'message'
        }
    """

    message: str
