"""
# Create Order Response

This module contains the response class for the Create Order API.

## Classes:

* `OrderInfo`: A `TypedDict` that represents the structure of the order information
* `CreateOrderResponse`: A `TypedDict` that represents the structure of the create order response
"""

from typing import TypedDict

from .coin_info import CoinInfo

__all__ = ["CreateOrderResponse", "OrderInfo"]


class OrderInfo(TypedDict):
    """
    Order Information.

    Attributes:
        id (int): ID.
        type (int): Type.
        each_price (str): Each price.
        stop_price (str): Stop price.
        trigger_price (str): Trigger price.
        amount (str): Amount.
        available_amount (str): Available amount.
        done_value (str): Done value.
        done_percent (str): Done percent.
        mean_value (int): Mean value.
        commission (str): Commission.
        total (str): Total.
        created_at (str): Created at.
        created_at_jalali (str): Created at jalali.
        base_coin (CoinInfo): Base coin.
        quote_coin (CoinInfo): Quote coin.
        status (int): Status.
        status_text (str): Status text.
        category_type (str): Category type.
        category_type_text (str): Category type text.
        conditions (str): Conditions.
        triggered_category_type (str): Triggered category type.
        is_trade (int): Is trade.

    Examples:
        >>> OrderInfo(
        ...     id=1,
        ...     type=1,
        ...     each_price="each_price",
        ...     stop_price="stop_price",
        ...     trigger_price="trigger_price",
        ...     amount="amount",
        ...     available_amount="available_amount",
        ...     done_value="done_value",
        ...     done_percent="done_percent",
        ...     mean_value=1,
        ...     commission="commission",
        ...     total="total",
        ...     created_at="created_at",
        ...     created_at_jalali="created_at_jalali",
        ...     base_coin=CoinInfo(
        ...         id=1,
        ...         symbol="symbol",
        ...         name="name",
        ...         fa_name="fa_name",
        ...         web_icon="web_icon",
        ...         app_icon="app_icon",
        ...     ),
        ...     quote_coin=CoinInfo(
        ...         id=1,
        ...         symbol="symbol",
        ...         name="name",
        ...         fa_name="fa_name",
        ...         web_icon="web_icon",
        ...         app_icon="app_icon",
        ...     ),
        ...     status=1,
        ...     status_text="status_text",
        ...     category_type="category_type",
        ...     category_type_text="category_type_text",
        ...     conditions="conditions",
        ...     triggered_category_type="triggered_category_type",
        ...     is_trade=1,
        ... )
        {
            "id": 1,
            "type": 1,
            "each_price": "each_price",
            "stop_price": "stop_price",
            "trigger_price": "trigger_price",
            "amount": "amount",
            "available_amount": "available_amount",
            "done_value": "done_value",
            "done_percent": "done_percent",
            "mean_value": 1,
            "commission": "commission",
            "total": "total",
            "created_at": "created_at",
            "created_at_jalali": "created_at_jalali",
            "base_coin": {
                "id": 1,
                "symbol": "symbol",
                "name": "name",
                "fa_name": "fa_name",
                "web_icon": "web_icon",
                "app_icon": "app_icon"
            },
            "quote_coin": {
                "id": 1,
                "symbol": "symbol",
                "name": "name",
                "fa_name": "fa_name",
                "web_icon": "web_icon",
                "app_icon": "app_icon"
            },
            "status": 1,
            "status_text": "status_text",
            "category_type": "category_type",
            "category_type_text": "category_type_text",
            "conditions": "conditions",
            "triggered_category_type": "triggered_category_type",
            "is_trade": 1
        }
    """

    id: int
    type: int
    each_price: str
    stop_price: str
    trigger_price: str
    amount: str
    available_amount: str
    done_value: str
    done_percent: str
    mean_value: int
    commission: str
    total: str
    created_at: str
    created_at_jalali: str
    base_coin: CoinInfo
    quote_coin: CoinInfo
    status: int
    status_text: str
    category_type: str
    category_type_text: str
    conditions: str
    triggered_category_type: str
    is_trade: int


class CreateOrderResponse(TypedDict):
    """
    Create Order Response.

    Attributes:
        message (str): Message.
        order (OrderInfo): Order.

    Examples:
        >>> CreateOrderResponse(
        ...     message="message",
        ...     order=OrderInfo(
        ...         id=1,
        ...         type=1,
        ...         each_price="each_price",
        ...         stop_price="stop_price",
        ...         trigger_price="trigger_price",
        ...         amount="amount",
        ...         available_amount="available_amount",
        ...         done_value="done_value",
        ...         done_percent="done_percent",
        ...         mean_value=1,
        ...         commission="commission",
        ...         total="total",
        ...         created_at="created_at",
        ...         created_at_jalali="created_at_jalali",
        ...         base_coin=CoinInfo(
        ...             id=1,
        ...             symbol="symbol",
        ...             name="name",
        ...             fa_name="fa_name",
        ...             web_icon="web_icon",
        ...             app_icon="app_icon",
        ...         ),
        ...         quote_coin=CoinInfo(
        ...             id=1,
        ...             symbol="symbol",
        ...             name="name",
        ...             fa_name="fa_name",
        ...             web_icon="web_icon",
        ...             app_icon="app_icon",
        ...         ),
        ...         status=1,
        ...         status_text="status_text",
        ...         category_type="category_type",
        ...         category_type_text="category_type_text",
        ...         conditions="conditions",
        ...         triggered_category_type="triggered_category_type",
        ...         is_trade=1,
        ...     ),
        ... )
        {
            "message": "message",
            "order": {
                "id": 1,
                "type": 1,
                "each_price": "each_price",
                "stop_price": "stop_price",
                "trigger_price": "trigger_price",
                "amount": "amount",
                "available_amount": "available_amount",
                "done_value": "done_value",
                "done_percent": "done_percent",
                "mean_value": 1,
                "commission": "commission",
                "total": "total",
                "created_at": "created_at",
                "created_at_jalali": "created_at_jalali",
                "base_coin": {
                    "id": 1,
                    "symbol": "symbol",
                    "name": "name",
                    "fa_name": "fa_name",
                    "web_icon": "web_icon",
                    "app_icon": "app_icon"
                },
                "quote_coin": {
                    "id": 1,
                    "symbol": "symbol",
                    "name": "name",
                    "fa_name": "fa_name",
                    "web_icon": "web_icon",
                    "app_icon": "app_icon"
                },
                "status": 1,
                "status_text": "status_text",
                "category_type": "category_type",
                "category_type_text": "category_type_text",
                "conditions": "conditions",
                "triggered_category_type": "triggered_category_type",
                "is_trade": 1
            }
        }
    """

    message: str
    order: OrderInfo
