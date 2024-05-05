"""
# Coin Info

This module contains the `CoinInfo` type hint which is a `TypedDict` that represents the structure of the coin information

## Classes

* `CoinInfo`: A `TypedDict` that represents the structure of the coin information
"""

from typing import TypedDict

__all__ = [
    "CoinInfo",
]


class CoinInfo(TypedDict):
    """
    Coin Information.

    Attributes:
        id (int): ID.
        symbol (str): Symbol.
        name (str): Name.
        fa_name (str): Fa name.
        web_icon (str): Web icon.
        app_icon (str): App icon.

    Examples:
        >>> CoinInfo(
        ...     id=1,
        ...     symbol="symbol",
        ...     name="name",
        ...     fa_name="fa_name",
        ...     web_icon="web_icon",
        ...     app_icon="app_icon",
        ... )
        {'id': 1, 'symbol': 'symbol', 'name': 'name', 'fa_name': 'fa_name', 'web_icon': 'web_icon', 'app_icon': 'app_icon'}
    """

    id: int
    symbol: str
    name: str
    fa_name: str
    web_icon: str
    app_icon: str
