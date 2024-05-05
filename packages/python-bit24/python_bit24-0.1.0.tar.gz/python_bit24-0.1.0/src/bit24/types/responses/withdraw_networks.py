"""
# Withdrawal Networks Response.

This module contains the type definitions for the response of the withdrawal networks endpoint.

## Classes

* `WithdrawNetworkInfo`: A `TypedDict` that represents the structure of the network information.
* `WithdrawalNetworksResponse`: A `TypedDict` that represents the structure of the withdrawal networks response.
"""

from typing import TypedDict

__all__ = ["WithdrawNetworkInfo", "WithdrawalNetworksResponse"]


class WithdrawNetworkInfo(TypedDict):
    """
    Network Information.

    Attributes:
        network_id (int): Network ID.
        network_name (str): Network name.
        network_layer (str): Network layer.
        min_withdraw (str): Min withdraw.
        max_withdraw (str): Max withdraw.
        fee (str): Fee.
        address_regex (str): Address regex.
        memo_regex (str): Memo regex.

    Examples:
        >>> WithdrawNetworkInfo(
        ...     network_id=1,
        ...     network_name="network_name",
        ...     network_layer="network_layer",
        ...     min_withdraw="min_withdraw",
        ...     max_withdraw="max_withdraw",
        ...     fee="fee",
        ...     address_regex="address_regex",
        ...     memo_regex="memo_regex",
        ... )
        {
            'network_id': 1,
            'network_name': 'network_name',
            'network_layer': 'network_layer',
            'min_withdraw': 'min_withdraw',
            'max_withdraw': 'max_withdraw',
            'fee': 'fee',
            'address_regex': 'address_regex',
            'memo_regex': 'memo_regex'
        }
    """

    network_id: int
    network_name: str
    network_layer: str
    min_withdraw: str
    max_withdraw: str | None
    fee: str
    address_regex: str
    memo_regex: str | None


class WithdrawalNetworksResponse(TypedDict):
    """
    Withdrawal Networks Response.

    Attributes:
        balance (str): Balance.
        networks (list[NetworkInfo]): Networks.

    Examples:
        >>> WithdrawalNetworksResponse(
        ...     balance="balance",
        ...     networks=[
        ...         WithdrawNetworkInfo(
        ...             network_id=1,
        ...             network_name="network_name",
        ...             network_layer="network_layer",
        ...             min_withdraw="min_withdraw",
        ...             max_withdraw="max_withdraw",
        ...             fee="fee",
        ...             address_regex="address_regex",
        ...             memo_regex="memo_regex",
        ...         )
        ...     ],
        ... )
        {
            'balance': 'balance',
            'networks': [
                {
                    'network_id': 1,
                    'network_name': 'network_name',
                    'network_layer': 'network_layer',
                    'min_withdraw': 'min_withdraw',
                    'max_withdraw': 'max_withdraw',
                    'fee': 'fee',
                    'address_regex': 'address_regex',
                    'memo_regex': 'memo_regex'
                }
            ]
        }
    """

    balance: str
    networks: list[WithdrawNetworkInfo]
