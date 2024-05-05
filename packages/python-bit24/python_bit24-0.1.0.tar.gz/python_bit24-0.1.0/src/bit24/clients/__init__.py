"""
# Clients

This package contains the clients for the different services that the application uses.

## Modules

* [Core](_core) - Core client.
* [Abstract](_abstract) - Abstract client.
* [Sync Client](client) - Sync client (use [requests](https://docs.python-requests.org/en/master/)).
* [Async Client](async_client) - Async client (use [aiohttp](https://docs.aiohttp.org/en/stable/)).
"""

__all__ = [
    "AsyncClient",
    "Client",
]

from .async_client import AsyncClient
from .client import Client
