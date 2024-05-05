"""
# Order Book Response

This file contains the Order Book Response.

## Classes:

* `OrderBookItem`: A `TypedDict` that represents the structure of the order book item.
* `OrderBookResponse`: A `TypedDict` that represents the structure of the order book response.
"""

from typing import TypedDict

__all__ = ["OrderBookItem", "OrderBookResponse"]


class OrderBookItem(TypedDict):
    """
    Order Book Item.

    Attributes:
        market_id (int): Market ID.
        each_price (str): Each price.
        available_amount (str): Available amount.

    Examples:
        >>> OrderBookItem(
        ...     market_id=1, each_price="each_price", available_amount="available_amount"
        ... )
        {
            'market_id': 1,
            'each_price': 'each_price',
            'available_amount': 'available_amount'
        }
    """

    market_id: int
    each_price: str
    available_amount: str


class OrderBookResponse(TypedDict):
    """
    Order Book Response.

    Attributes:
        id (int): ID.
        market_symbol (str): Market symbol.
        buy_orders (list[OrderBookItem]): Buy orders.
        sell_orders (list[OrderBookItem]): Sell orders.

    Examples:
        >>> OrderBookResponse(
        ...     id=1,
        ...     market_symbol="market_symbol",
        ...     buy_orders=[
        ...         OrderBookItem(
        ...             market_id=1,
        ...             each_price="each_price",
        ...             available_amount="available_amount",
        ...         )
        ...     ],
        ...     sell_orders=[
        ...         OrderBookItem(
        ...             market_id=1,
        ...             each_price="each_price",
        ...             available_amount="available_amount",
        ...         )
        ...     ],
        ... )
        {
            'id': 1,
            'market_symbol': 'market_symbol',
            'buy_orders': [
                {
                    'market_id': 1,
                    'each_price': 'each_price',
                    'available_amount': 'available_amount'
                }
            ],
            'sell_orders': [
                {
                    'market_id': 1,
                    'each_price': 'each_price',
                    'available_amount': 'available_amount'
                }
            ]
        }
    """

    id: int
    market_symbol: str
    buy_orders: list[OrderBookItem]
    sell_orders: list[OrderBookItem]
