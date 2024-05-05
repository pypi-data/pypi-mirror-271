"""
# Assets history.

This module contains the data classes for the assets history response.

## Classes:

* `Transaction`: A `TypedDict` that represents the structure of the transaction
* `AssetsHistoryResponse`: A `TypedDict` that represents the structure of the assets history response
"""

from typing import TypedDict

__all__ = ["AssetsHistoryResponse", "Transaction"]


class Transaction(TypedDict):
    """
    Transaction.

    Attributes:
        id (int): ID.
        name (str): Name.
        fa_name (str): Fa name.
        symbol (str): Symbol.
        logo (str): Logo.
        value (str): Value.
        done_value (str): Done value.
        type (int): Type.
        transaction_code (str): Transaction code.
        type_text (str): Type text.
        reason_type (str): Reason type.
        reason_text (str): Reason text.
        reason_type_text (str): Reason type text.
        reason_id (int): Reason ID.
        balance_status (int): Balance status.
        balance_status_text (str): Balance status text.
        commission (int): Commission.
        created_at (str): Created at.
        created_at_jalali (str): Created at jalali.

    Examples:
        >>> Transaction(
        ...     id=1,
        ...     name="name",
        ...     fa_name="fa_name",
        ...     symbol="symbol",
        ...     logo="logo",
        ...     value="value",
        ...     done_value="done_value",
        ...     type=1,
        ...     transaction_code="transaction_code",
        ...     type_text="type_text",
        ...     reason_type="reason_type",
        ...     reason_text="reason_text",
        ...     reason_type_text="reason_type_text",
        ...     reason_id=1,
        ...     balance_status=1,
        ...     balance_status_text="balance_status_text",
        ...     commission=1,
        ...     created_at="created_at",
        ...     created_at_jalali="created_at_jalali",
        ... )
        {
            "id": 1,
            "name": "name",
            "fa_name": "fa_name",
            "symbol": "symbol",
            "logo": "logo",
            "value": "value",
            "done_value": "done_value",
            "type": 1,
            "transaction_code": "transaction_code",
            "type_text": "type_text",
            "reason_type": "reason_type",
            "reason_text": "reason_text",
            "reason_type_text": "reason_type_text",
            "reason_id": 1,
            "balance_status": 1,
            "balance_status_text": "balance_status_text",
            "commission": 1,
            "created_at": "created_at",
            "created_at_jalali": "created_at_jalali"
        }
    """

    id: int
    name: str
    fa_name: str
    symbol: str
    logo: str
    value: str
    done_value: str
    type: int
    transaction_code: str
    type_text: str
    reason_type: str
    reason_text: str
    reason_type_text: str
    reason_id: int
    balance_status: int
    balance_status_text: str
    commission: int
    created_at: str
    created_at_jalali: str


class AssetsHistoryResponse(TypedDict):
    """
    Assets history response.

    Attributes:
        message (str): Message.
        has_paginate (int): Has paginate.
        total_data (int): Total data.
        current_page (int): Current page.
        from_ (int): From.
        to (int): To.
        per_page (int): Per page.
        results (list[Transaction]): Results.

    Examples:
        >>> AssetsHistoryResponse(
        ...     message="message",
        ...     has_paginate=1,
        ...     total_data=1,
        ...     current_page=1,
        ...     from_=1,
        ...     to=1,
        ...     per_page=1,
        ...     results=[
        ...         {
        ...             "id": 1,
        ...             "name": "name",
        ...             "fa_name": "fa_name",
        ...             "symbol": "symbol",
        ...             "logo": "logo",
        ...             "value": "value",
        ...             "done_value": "done_value",
        ...             "type": 1,
        ...             "transaction_code": "transaction_code",
        ...             "type_text": "type_text",
        ...             "reason_type": "reason_type",
        ...             "reason_text": "reason_text",
        ...             "reason_type_text": "reason_type_text",
        ...             "reason_id": 1,
        ...             "balance_status": 1,
        ...             "balance_status_text": "balance_status_text",
        ...             "commission": 1,
        ...             "created_at": "created_at",
        ...             "created_at_jalali": "created_at_jalali",
        ...         }
        ...     ],
        ... )
        {
            "message": "message",
            "has_paginate": 1,
            "total_data": 1,
            "current_page": 1,
            "from_": 1,
            "to": 1,
            "per_page": 1,
            "results": [
                {
                    "id": 1,
                    "name": "name",
                    "fa_name": "fa_name",
                    "symbol": "symbol",
                    "logo": "logo",
                    "value": "value",
                    "done_value": "done_value",
                    "type": 1,
                    "transaction_code": "transaction_code",
                    "type_text": "type_text",
                    "reason_type": "reason_type",
                    "reason_text": "reason_text",
                    "reason_type_text": "reason_type_text",
                    "reason_id": 1,
                    "balance_status": 1,
                    "balance_status_text": "balance_status_text",
                    "commission": 1,
                    "created_at": "created_at",
                    "created_at_jalali": "created_at_jalali"
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
    results: list[Transaction]
