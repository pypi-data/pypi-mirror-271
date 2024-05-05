"""
# Exceptions.

Exceptions for the bit24 package.

## Classes:

* `APIError`: API Exception.
* `RequestError`: Request Exception.
"""

import json
from typing import TYPE_CHECKING, Any

from . import types as t

if TYPE_CHECKING:
    from .types import responses as rt


class APIError(Exception):
    """
    API Exception.

    Attributes:
        url (str): URL.
        request (t.Http): Request.
        response (t.HttpResponse): Response.
        message: (str): Message.
    """

    def __init__(self, response: t.HttpResponse, status_code: int, text: str):
        """
        Constructor.

        Args:
            response (HttpResponse): Response.
            status_code (int): Status code.
            text (str): Text.
        """
        self.request = getattr(response, "request", None)
        self.url = getattr(response, "url", None)
        self.response = response

        try:
            json_res: rt.BaseResponse = json.loads(text)
        except ValueError:
            self.message = f"Invalid JSON error message from Bit24: {response.text}"
        else:
            error: rt.Error | dict[str, Any] = json_res.get("error", {}) or {}
            self.status_code = json_res.get("status_code", status_code)
            self.message = error.get("message", "Unknown error") or "Unknown error"
            self.errors = error.get("errors", []) or []

    def __str__(self) -> str:
        """
        String representation.

        Returns:
            str: String representation.
        """
        return f"APIError(code={self.status_code}): '{self.message}' | Errors: {self.errors}"


class RequestError(Exception):
    """
    Request Exception.

    Attributes:
        message (str): Message.
    """

    def __init__(self, message: str):
        """
        Constructor.

        Args:
            message (str): Message.
        """
        self.message = message

    def __str__(self) -> str:
        """
        String representation.

        Returns:
            str: String representation.
        """
        return f"RequestError: {self.message}"
