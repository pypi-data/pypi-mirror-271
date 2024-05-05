"""
# Orders History Response

This module contains the type definitions for the response of the orders history endpoint.

## Classes

* `OrdersHistoryResponse`: A `TypedDict` that represents the structure of the orders history response.
"""

from typing import TypedDict

from .create_order import OrderInfo

__all__ = ["OrdersHistoryResponse"]


class OrdersHistoryResponse(TypedDict):
    """
    Orders History Response.

    Attributes:
        message (str): Message.
        has_paginate (int): Has paginate.
        total_data (int): Total data.
        current_page (int): Current page.
        from_ (int): From.
        to( int): To.
        per_page (int): Per page.
        results (list[OrderInfo]): Results.

    Examples:
        >>> OrdersHistoryResponse(
        ...     message="message",
        ...     has_paginate=1,
        ...     total_data=1,
        ...     current_page=1,
        ...     from_=1,
        ...     to=1,
        ...     per_page=1,
        ...     results=[...],  # OrderInfo
        ... )
        {
            'message': 'message',
            'has_paginate': 1,
            'total_data': 1,
            'current_page': 1,
            'from_': 1,
            'to': 1,
            'per_page': 1,
            'results': [...] # OrderInfo
        }
    """

    message: str
    has_paginate: int
    total_data: int
    current_page: int
    from_: int
    to: int
    per_page: int
    results: list[OrderInfo]
