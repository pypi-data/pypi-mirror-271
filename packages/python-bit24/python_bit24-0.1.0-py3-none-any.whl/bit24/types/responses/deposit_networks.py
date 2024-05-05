"""
# Deposit Networks

This module contains the type definitions for the response of the deposit networks endpoint.

## Classes

* `DepositNetworkInfo`: A `TypedDict` that represents the structure of the network information
* `DepositNetworksResponse`: A `TypedDict` that represents the structure of the deposit networks response
"""

from typing import TypedDict

__all__ = ["DepositNetworkInfo", "DepositNetworksResponse"]


class DepositNetworkInfo(TypedDict):
    """
    Network Information.

    Attributes:
        network_name  (str): Network name.
        network_layer (str): Network layer.
        description_deposit (str): Description deposit.
        min_deposit (str): Min deposit.
        address (str): Address.
        memo (str): Memo.

    Examples:
        >>> DepositNetworkInfo(
        ...     network_name="network_name",
        ...     network_layer="network_layer",
        ...     description_deposit="description_deposit",
        ...     min_deposit="min_deposit",
        ...     address="address",
        ...     memo="memo",
        ... )
        {
            'network_name': 'network_name',
            'network_layer': 'network_layer',
            'description_deposit': 'description_deposit',
            'min_deposit': 'min_deposit',
            'address': 'address',
            'memo': 'memo'
        }
    """

    network_name: str
    network_layer: str
    description_deposit: str
    min_deposit: str
    address: str
    memo: str | None


class DepositNetworksResponse(TypedDict):
    """
    Deposit Networks Response.

    Attributes:
        networks (list[DepositNetworkInfo]): Networks.

    Examples:
        >>> DepositNetworksResponse(
        ...     networks=[
        ...         DepositNetworkInfo(
        ...             network_name="network_name",
        ...             network_layer="network_layer",
        ...             description_deposit="description_deposit",
        ...             min_deposit="min_deposit",
        ...             address="address",
        ...             memo="memo",
        ...         )
        ...     ]
        ... )
        {
            'networks': [
                {
                    'network_name': 'network_name',
                    'network_layer': 'network_layer',
                    'description_deposit': 'description_deposit',
                    'min_deposit': 'min_deposit',
                    'address': 'address',
                    'memo': 'memo'
                }
            ]
        }
    """

    networks: list[DepositNetworkInfo]
