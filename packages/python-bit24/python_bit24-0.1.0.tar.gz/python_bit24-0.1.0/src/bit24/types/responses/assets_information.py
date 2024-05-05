"""
# Assets Information

This module contains the data classes for the assets information response.

##  Classes:

* `AssetMarketInfo`: A `TypedDict` that represents the structure of the market information
* `AssetInfo`: A `TypedDict` that represents the structure of the asset information
* `AssetInformationResponse`: A `TypedDict` that represents the structure of the asset information response
"""

from typing import TypedDict

from .coin_info import CoinInfo

__all__ = ["AssetInfo", "AssetInformationResponse", "AssetMarketInfo"]


class AssetMarketInfo(TypedDict):
    """
    Market Information.

    Attributes:
        base_coin_symbol (str): Base coin symbol.
        quote_coin_symbol (str): Quote coin symbol.
        is_active (int): Is active.

    Examples:
        >>> AssetMarketInfo(
        ...     base_coin_symbol="base_coin_symbol",
        ...     quote_coin_symbol="quote_coin_symbol",
        ...     is_active=1,
        ... )
        {
            'base_coin_symbol': 'base_coin_symbol',
            'quote_coin_symbol': 'quote_coin_symbol',
            'is_active': 1
        }
    """

    base_coin_symbol: str
    quote_coin_symbol: str
    is_active: int


class AssetInfo(TypedDict, CoinInfo):
    """
    Asset Information.

    Attributes:
        coin_type (int): Coin type.
        each_price (str): Each price.
        change_24hr (str): Change 24hr.
        balance (str): Balance.
        available_balance (str): Available balance.
        in_orders (str): In orders.
        balance_irt (str): Balance IRT.
        balance_usdt (str): Balance USDT.
        markets (list[AssetMarketInfo]): Markets.

    Examples:
        >>> AssetInfo(
        ...     coin_type=1,
        ...     each_price="each_price",
        ...     change_24hr="change_24hr",
        ...     balance="balance",
        ...     available_balance="available_balance",
        ...     in_orders="in_orders",
        ...     balance_irt="balance_irt",
        ...     balance_usdt="balance_usdt",
        ...     markets=[...],  # AssetMarketInfo
        ... )
        {
            'coin_type': 1,
            'each_price': 'each_price',
            'change_24hr': 'change_24hr',
            'balance': 'balance',
            'available_balance': 'available_balance',
            'in_orders': 'in_orders',
            'balance_irt': 'balance_irt',
            'balance_usdt': 'balance_usdt',
            'markets': [...] # AssetMarketInfo
        }
    """

    coin_type: int
    each_price: str
    change_24hr: str
    balance: str
    available_balance: str
    in_orders: str
    balance_irt: str
    balance_usdt: str
    markets: list[AssetMarketInfo]


class AssetInformationResponse(TypedDict):
    """
    Asset Information Response.

    Attributes:
        message (str): Message.
        asset (list[AssetInfo]): Asset.

    Examples:
        >>> AssetInformationResponse(
        ...     message="message",
        ...     asset=[...],  # AssetInfo
        ... )
        {
            'message': 'message',
            'asset': [...] # AssetInfo
        }
    """

    message: str
    asset: list[AssetInfo]
