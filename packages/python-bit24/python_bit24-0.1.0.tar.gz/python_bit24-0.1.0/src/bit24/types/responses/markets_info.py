"""
# Markets Info

This module contains the type hints for the response of the `markets` endpoint.

## Classes:

* `MarketInfo`: A `TypedDict` that represents the structure of the market information.
* `MarketListResponse`: A `TypedDict` that represents the structure of the market list response.
"""

from typing import TypedDict

__all__ = ["MarketInfo", "MarketListResponse"]


class MarketInfo(TypedDict):
    """
    Market Information.

    Attributes:
        id (int): Market ID.
        base_coin_id (int): Base coin ID.
        base_coin_name (str): Base coin name.
        base_coin_fa_name (str): Base coin Farsi name.
        base_coin_symbol (str): Base coin symbol.
        quote_coin_id (int): Quote coin ID.
        quote_coin_symbol (str): Quote coin symbol.
        quote_coin_name (str): Quote coin name.
        quote_coin_fa_name (str): Quote coin Farsi name.
        each_price (str): Each price.
        other_side_each_price (str): Other side each price.
        quote_coin_volume (str): Quote coin volume.
        base_coin_volume (str): Base coin volume.
        _24h_change (str): 24-hour change.
        _24h_change_volume (str): 24-hour change volume.
        total_min (str): Total min.
        market_order_quote_coin_total_min (str): Market order quote coin total min.
        market_order_base_coin_total_min (str): Market order base coin total min.
        web_icon (str): Web icon.
        app_icon (str): App icon.
        quote_web_icon (str): Quote web icon.
        quote_app_icon (str): Quote app icon.
        is_active (int): Is active.
        first_order (str): First order.
        last_order (str): Last order.
        min_price (str): Min price.
        max_price (str): Max price.
        base_coin_decimal (int): Base coin decimal.
        quote_coin_decimal (int): Quote coin decimal.
        daily_chart_icon (str): Daily chart icon.
        is_favorite (bool): Is favorite.

    Examples:
        >>> MarketInfo(
        ...     id=1,
        ...     base_coin_id=1,
        ...     base_coin_name="base_coin_name",
        ...     base_coin_fa_name="base_coin_fa_name",
        ...     base_coin_symbol="base_coin_symbol",
        ...     quote_coin_id=1,
        ...     quote_coin_symbol="quote_coin_symbol",
        ...     quote_coin_name="quote_coin_name",
        ...     quote_coin_fa_name="quote_coin_fa_name",
        ...     each_price="each_price",
        ...     other_side_each_price="other_side_each_price",
        ...     quote_coin_volume="quote_coin_volume",
        ...     base_coin_volume="base_coin_volume",
        ...     _24h_change="_24h_change",
        ...     _24h_change_volume="_24h_change_volume",
        ...     total_min="total_min",
        ...     market_order_quote_coin_total_min="market_order_quote_coin_total_min",
        ...     market_order_base_coin_total_min="market_order_base_coin_total_min",
        ...     web_icon="web_icon",
        ...     app_icon="app_icon",
        ...     quote_web_icon="quote_web_icon",
        ...     quote_app_icon="quote_app_icon",
        ...     is_active=1,
        ...     first_order="first_order",
        ...     last_order="last_order",
        ...     min_price="min_price",
        ...     max_price="max_price",
        ...     base_coin_decimal=1,
        ...     quote_coin_decimal=1,
        ...     daily_chart_icon="daily_chart_icon",
        ...     is_favorite=True,
        ... )
        {
            'id': 1,
            'base_coin_id': 1,
            'base_coin_name': 'base_coin_name',
            'base_coin_fa_name': 'base_coin_fa_name',
            'base_coin_symbol': 'base_coin_symbol',
            'quote_coin_id': 1,
            'quote_coin_symbol': 'quote_coin_symbol',
            'quote_coin_name': 'quote_coin_name',
            'quote_coin_fa_name': 'quote_coin_fa_name',
            'each_price': 'each_price',
            'other_side_each_price': 'other_side_each_price',
            'quote_coin_volume': 'quote_coin_volume',
            'base_coin_volume': 'base_coin_volume',
            '_24h_change': '_24h_change',
            '_24h_change_volume': '_24h_change_volume',
            'total_min': 'total_min',
            'market_order_quote_coin_total_min': 'market_order_quote_coin_total_min',
            'market_order_base_coin_total_min': 'market_order_base_coin_total_min',
            'web_icon': 'web_icon',
            'app_icon': 'app_icon',
            'quote_web_icon': 'quote_web_icon',
            'quote_app_icon': 'quote_app_icon',
            'is_active': 1,
            'first_order': 'first_order',
            'last_order': 'last_order',
            'min_price': 'min_price',
            'max_price': 'max_price',
            'base_coin_decimal': 1,
            'quote_coin_decimal': 1,
            'daily_chart_icon': 'daily_chart_icon',
            'is_favorite': True
        }
    """

    id: int
    base_coin_id: int
    base_coin_name: str
    base_coin_fa_name: str
    base_coin_symbol: str
    quote_coin_id: int
    quote_coin_symbol: str
    quote_coin_name: str
    quote_coin_fa_name: str
    each_price: str
    other_side_each_price: str
    quote_coin_volume: str
    base_coin_volume: str
    _24h_change: str
    _24h_change_volume: str
    total_min: str
    market_order_quote_coin_total_min: str
    market_order_base_coin_total_min: str
    web_icon: str
    app_icon: str
    quote_web_icon: str
    quote_app_icon: str
    is_active: int
    first_order: str
    last_order: str
    min_price: str
    max_price: str
    base_coin_decimal: int
    quote_coin_decimal: int
    daily_chart_icon: str
    is_favorite: bool


class MarketListResponse(TypedDict):
    """
    Market List Response.

    Attributes:
        message (str): Message.
        has_paginate (int): Has paginate.
        total_data (int): Total data.
        current_page (int): Current page.
        from_ (int): From.
        to (int): To.
        per_page (int): Per page.
        results (list[MarketInfo]): Results.

    Examples:
        >>> MarketListResponse(
        ...     message="message",
        ...     has_paginate=1,
        ...     total_data=1,
        ...     current_page=1,
        ...     from_=1,
        ...     to=1,
        ...     per_page=1,
        ...     results=[
        ...         MarketInfo(
        ...             id=1,
        ...             base_coin_id=1,
        ...             base_coin_name="base_coin_name",
        ...             base_coin_fa_name="base_coin_fa_name",
        ...             base_coin_symbol="base_coin_symbol",
        ...             quote_coin_id=1,
        ...             quote_coin_symbol="quote_coin_symbol",
        ...             quote_coin_name="quote_coin_name",
        ...             quote_coin_fa_name="quote_coin_fa_name",
        ...             each_price="each_price",
        ...             other_side_each_price="other_side_each_price",
        ...             quote_coin_volume="quote_coin_volume",
        ...             base_coin_volume="base_coin_volume",
        ...             _24h_change="_24h_change",
        ...             _24h_change_volume="_24h_change_volume",
        ...             total_min="total_min",
        ...             market_order_quote_coin_total_min="market_order_quote_coin_total_min",
        ...             market_order_base_coin_total_min="market_order_base_coin_total_min",
        ...             web_icon="web_icon",
        ...             app_icon="app_icon",
        ...             quote_web_icon="quote_web_icon",
        ...             quote_app_icon="quote_app_icon",
        ...             is_active=1,
        ...             first_order="first_order",
        ...             last_order="last_order",
        ...             min_price="min_price",
        ...             max_price="max_price",
        ...             base_coin_decimal=1,
        ...             quote_coin_decimal=1,
        ...             daily_chart_icon="daily_chart_icon",
        ...             is_favorite=True
        ...     ]
        ... )
        {
            'message': 'message',
            'has_paginate': 1,
            'total_data': 1,
            'current_page': 1,
            'from': 1,
            'to': 1,
            'per_page': 1,
            'results': [
                {
                    'id': 1,
                    'base_coin_id': 1,
                    'base_coin_name
                    ...
                }
            ]
        }
    """

    message: str
    has_paginate: int
    total_data: int
    current_page: int
    from_: int
    to: int
    per_page: int
    results: list[MarketInfo]
