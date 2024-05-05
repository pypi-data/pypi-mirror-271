"""
# Core Client

This module contains the core client class that is used by the main client class.
"""

import hmac
from hashlib import sha256
from operator import itemgetter
from typing import Any

from .. import enums


class CoreClient:
    """
    Core client class that contains the base URL and the API version.

    Attributes:
        BASE_URL (str): The base URL of the API.
        API_VERSION (str): The API version.
        REQUEST_TIMEOUT (int): The request timeout.
        WITHDRAW_NETWORKS_URI (str): The URI for getting the withdrawal networks.
        SUBMIT_WITHDRAW_URI (str): The URI for submitting a withdrawal.
        DEPOSIT_NETWORKS_URI (str): The URI for getting the deposit networks.
        ASSETS_INFORMATION_URI (str): The URI for getting the assets' information.
        ASSETS_HISTORY_URI (str): The URI for getting the assets' history.
        CREATE_ORDER_URI (str): The URI for creating an order.
        CANCEL_ORDER_URI (str): The URI for cancelling an order.
        ORDERS_HISTORY_URI (str): The URI for getting the orders' history.
        MARKETS_INFORMATION_URI (str): The URI for getting the markets' information.
        ORDER_BOOK_URI (str): The URI for getting the order book.

    Args:
        api_key (str): The API key.
        api_secret (str | None): The API secret.
        session_params (Optional[Dict[str, Any]]): The session parameters.
        requests_params (Optional[Dict[str, Any]]): The requests parameters.

    Methods:
        _get_headers: Get the headers.
        _get_request_kwargs: Get the request keyword arguments.
        _hmac_signature: Generate the HMAC signature.
        _order_params: Order the parameters.
        _generate_signature: Generate the signature.
        _create_api_uri: Create the API URI.
        _get_kwargs_from_locals: Get the keyword arguments from the locals.

    Examples:
        >>> client = CoreClient("api_key", "api_secret")
    """

    BASE_URL: str = "https://rest.bit24.cash"

    API_VERSION: str = "v1"

    REQUEST_TIMEOUT: int = 10

    WITHDRAW_NETWORKS_URI: str = "lite/capi/{}/withdraw/networks"
    SUBMIT_WITHDRAW_URI: str = "lite/capi/{}/withdraw/submit"
    DEPOSIT_NETWORKS_URI: str = "lite/capi/{}/deposit/networks"
    ASSETS_INFORMATION_URI: str = "pro/capi/{}/wallet/assets"
    ASSETS_HISTORY_URI: str = "pro/capi/{}/wallet/assets/history"
    CREATE_ORDER_URI: str = "pro/capi/{}/orders/submit"
    CANCEL_ORDER_URI: str = "pro/capi/{}/orders/cancel"
    ORDERS_HISTORY_URI: str = "pro/capi/{}/orders/get-history"
    MARKETS_INFORMATION_URI: str = "pro/capi/{}/markets"
    ORDER_BOOK_URI: str = "pro/capi/{}/markets/orderbooks"

    def __init__(
        self,
        api_key: str,
        api_secret: str | None = None,
        session_params: dict[str, Any] | None = None,
        requests_params: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize the core client.

        Args:
            api_key (str): The API key.
            api_secret (str | None): The API secret.
            session_params (dict[str, Any] | None): The session parameters.
            requests_params (dict[str, Any] | None): The requests parameters.
        """
        self.API_KEY = api_key
        self.API_SECRET = api_secret

        self._session_params = session_params or {}
        self._requests_params = requests_params or {}

    def _get_headers(self) -> dict[str, str]:
        """
        (Private)

        Get the headers.

        Returns:
            dict[str, str]: The headers.
        """
        return {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-BIT24-APIKEY": self.API_KEY,
        }

    def _get_request_kwargs(
        self, method: enums.HTTPMethod | str, signed: bool, **kwargs: Any
    ) -> dict[str, Any]:
        """
        (Private)

        Get the request keyword arguments.

        Args:
            method (HTTPMethod | str): The HTTP method.
            signed (bool): If the request is signed.
            **kwargs (Any): The keyword arguments.

        Returns:
            Dict[str, Any]: The request keyword arguments.
        """
        kwargs["timeout"] = self.REQUEST_TIMEOUT

        if self._requests_params:
            kwargs.update(self._requests_params)

        data = kwargs.get("data", None)
        if data and isinstance(data, dict):
            kwargs["data"] = data

            if "requests_params" in kwargs["data"]:
                kwargs.update(kwargs["data"]["requests_params"])
                del kwargs["data"]["requests_params"]

        if signed is True:
            kwargs["data"]["signature"] = self._generate_signature(kwargs["data"])

        if data:
            kwargs["data"] = self._order_params(kwargs["data"])
            null_args = [
                i for i, (key, value) in enumerate(kwargs["data"]) if value is None
            ]
            for i in reversed(null_args):
                del kwargs["data"][i]
            kwargs["data"] = "&".join([f"{d[0]}={d[1]}" for d in kwargs["data"]])

        if data and method == enums.HTTPMethod.GET:
            kwargs["params"] = "&".join(
                f"{data[0]}={data[1]}" for data in kwargs["data"]
            )
            del kwargs["data"]

        return kwargs

    def _hmac_signature(self, query_string: str) -> str:
        """
        (Private)

        Generate the HMAC signature.

        Args:
            query_string (str): The query string.

        Returns:
            str: The HMAC signature.
        """
        assert self.API_SECRET, "API Secret required for private endpoints"
        return hmac.new(
            self.API_SECRET.encode("utf-8"), query_string.encode("utf-8"), sha256
        ).hexdigest()

    @staticmethod
    def _order_params(data: dict[str, Any]) -> list[tuple[str, str]]:
        """
        (Private, Static)

        Order the parameters.

        Args:
            data (Dict[str, Any]): The data.

        Returns:
            List[Tuple[str, str]]: The ordered parameters.

        """
        data = dict(filter(lambda el: el[1] is not None, data.items()))
        has_signature = False
        params = []
        for key, value in data.items():
            if key == "signature":
                has_signature = True
            else:
                params.append((key, str(value)))
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(("signature", data["signature"]))
        return params

    def _generate_signature(self, data: dict[str, Any]) -> str:
        """
        (Private)

        Generate the signature.

        Args:
            data (Dict[str, Any]): The data.

        Returns:
            str: The signature.
        """
        query_string = "&".join([f"{d[0]}={d[1]}" for d in self._order_params(data)])
        return self._hmac_signature(query_string)

    def _create_api_uri(self, path: str, version: str = API_VERSION) -> str:
        """
        (Private)

        Create the API URI.

        Args:
            path (str): The path.
            version (str): The version.

        Returns:
            str: The API URI.
        """
        return self.BASE_URL + "/" + path.format(version)

    @staticmethod
    def _get_kwargs_from_locals(
        locals_: dict[str, Any],
        exclude: list[str] | None = None,
        exclude_none: bool = True,
    ) -> dict[str, Any]:
        """
        (Private, Static)

        Get the keyword arguments from the locals.

        Args:
            locals_ (Dict[str, Any]): The locals.
            exclude (List[str]): The exclude list.
            exclude_none (bool): If exclude None.

        Returns:
            Dict[str, Any]: The keyword arguments.
        """
        if exclude is None:
            exclude = ["self", "kwargs"]

        return {
            key: value
            for key, value in locals_.items()
            if key not in exclude and (not exclude_none or value is not None)
        }
