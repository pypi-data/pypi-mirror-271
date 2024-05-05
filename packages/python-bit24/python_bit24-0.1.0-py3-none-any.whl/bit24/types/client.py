"""
# Client Type

This module contains the type hints for the client.

## Types

* `HttpSession`: The HTTP session type.
* `HttpResponse`: The HTTP response type.
* `HttpPreparedRequest`: The HTTP prepared request type.
"""

__all__ = [
    "HttpPreparedRequest",
    "HttpResponse",
    "HttpSession",
]

from aiohttp import ClientRequest, ClientResponse, ClientSession
from requests import Request, Response, Session

HttpSession = ClientSession | Session
HttpResponse = ClientResponse | Response
HttpPreparedRequest = ClientRequest | Request
