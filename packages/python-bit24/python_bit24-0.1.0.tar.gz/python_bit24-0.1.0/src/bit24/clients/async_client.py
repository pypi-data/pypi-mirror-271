"""
# Async Client

This module contains the main client class that is used to interact with the API.

## Classes

* `AsyncClient`: The main client class.
"""

import asyncio
from typing import Any

import aiohttp

from .. import enums
from .._utils import get_loop
from ..exceptions import APIError, RequestError
from ..types import responses as rt
from ._abstract import AbstractClient
from ._core import CoreClient


class AsyncClient(AbstractClient, CoreClient):
    """
    Main client class that is used to interact with the API.

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

    Methods:
        _get_headers: Get the headers.
        _get_request_kwargs: Get the request keyword arguments.
        _hmac_signature: Generate the HMAC signature.
        _order_params: Order the parameters.
        _generate_signature: Generate the signature.
        _create_api_uri: Create the API URI.
        _get_kwargs_from_locals: Get the keyword arguments from the locals.
        _init_session: Initialize the session.
        _request: Make a request.
        _request_api: Make a request to the API.
        _get: Make a GET request to the API.
        _post: Make a POST request to the API.
        _handle_response: Handle the response.
        get_withdraw_networks: Get the withdrawal networks.
        submit_withdraw: Submit a withdrawal.
        get_deposit_networks: Get the deposit networks.
        get_assets_information: Get the assets' information.
        get_assets_history: Get the assets' history.
        create_order: Create an order.
        cancel_order: Cancel an order.
        get_orders_history: Get the orders' history.
        get_markets_information: Get the markets' information.
        get_order_book: Get the order book.

    Args:
        api_key (str): The API key.
        api_secret (str | None): The API secret.
        session_params (Optional[Dict[str, Any]]): The session parameters.
        requests_params (Optional[Dict[str, Any]]): The requests parameters.
    """

    def __init__(  # noqa: PLR0913
        self,
        api_key: str,
        api_secret: str | None = None,
        session_params: dict[str, Any] | None = None,
        requests_params: dict[str, Any] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        """
        Initialize the core client.

        Args:
            api_key (str): The API key.
            api_secret (str | None): The API secret.
            session_params (dict[str, Any] | None): The session parameters.
            requests_params (dict[str, Any] | None): The requests parameters.
            loop (Optional[AbstractEventLoop]): The event loop.
        """
        super().__init__(api_key, api_secret, session_params, requests_params)
        self.loop = loop or get_loop()
        self.session = self._init_session()

    def _init_session(self) -> aiohttp.ClientSession:
        """
        (Private)

        Initialize the session.

        Returns:
            ClientSession: The session.
        """
        return aiohttp.ClientSession(
            loop=self.loop,
            headers=self._get_headers(),
            **self._session_params,
        )

    async def _request(  # type: ignore[override]
        self,
        method: enums.HTTPMethod | str,
        uri: str,
        signed: bool = False,
        **kwargs: Any,
    ) -> rt.BaseResponse:
        """
        (Private)

        Make a request to the API.

        Args:
            method (HTTPMethod | str): The HTTP method.
            uri (str): The URI.
            signed (bool): If the request is signed.
            **kwargs (Any): The keyword arguments.

        Returns:
            BaseResponse: The response.
        """
        kwargs = self._get_request_kwargs(method, signed, **kwargs)

        async with getattr(self.session, method.lower())(uri, **kwargs) as response:
            return await self._handle_response(response)

    async def _request_api(  # type: ignore[override]
        self,
        method: enums.HTTPMethod | str,
        path: str,
        signed: bool = False,
        version: str = CoreClient.API_VERSION,
        **kwargs: Any,
    ) -> rt.BaseResponse:
        """
        (Private)

        Make a request to the API.

        Args:
            method (HTTPMethod | str): The HTTP method.
            path (str): The path.
            signed (bool): If the request is signed.
            version (str): The API version.
            **kwargs (Any): The keyword arguments.

        Returns:
            BaseResponse: The response.
        """
        uri = self._create_api_uri(path, version)
        return await self._request(method, uri, signed, **kwargs)

    async def _get(  # type: ignore[override]
        self,
        path: str,
        signed: bool = False,
        version: str = CoreClient.API_VERSION,
        **kwargs: Any,
    ) -> rt.BaseResponse:
        """
        (Private)

        Make a GET request to the API.

        Args:
            path (str): The path.
            signed (bool): If the request is signed.
            version (str): The API version.
            **kwargs (Any): The keyword arguments.

        Returns:
            BaseResponse: The response.
        """
        return await self._request_api(
            enums.HTTPMethod.GET, path, signed, version, **kwargs
        )

    async def _post(  # type: ignore[override]
        self,
        path: str,
        signed: bool = False,
        version: str = CoreClient.API_VERSION,
        **kwargs: Any,
    ) -> rt.BaseResponse:
        """
        (Private)

        Make a POST request to the API.

        Args:
            path (str): The path.
            signed (bool): If the request is signed.
            version (str): The API version.
            **kwargs (Any): The keyword arguments.

        Returns:
            BaseResponse: The response.
        """
        return await self._request_api(
            enums.HTTPMethod.POST, path, signed, version, **kwargs
        )

    @staticmethod
    async def _handle_response(response: aiohttp.ClientResponse) -> rt.BaseResponse:  # type: ignore[override]
        """
        (Private)

        Handle the response.

        Args:
            response (HttpResponse): The response.

        Returns:
            BaseResponse: The response.
        """
        if not str(response.status).startswith("2"):
            raise APIError(response, response.status, await response.text())
        try:
            _: rt.BaseResponse = await response.json()
        except ValueError as exc:
            msg = f"Invalid Response: {await response.text()}"
            raise RequestError(msg) from exc
        else:
            return _

    async def get_withdraw_networks(  # type: ignore[override]
        self, symbol: str, **kwargs: Any
    ) -> rt.BaseResponse[rt.WithdrawalNetworksResponse]:
        """
        Get the withdrawal networks.

        Args:
            symbol (str): The symbol.
            kwargs (Any): The keyword arguments.

        Returns:
            BaseResponse[WithdrawalNetworksResponse]: The response.

        Raises:
            APIError: An error occurred.
            RequestError: An error occurred.
        """
        kwargs["params"] = self._get_kwargs_from_locals(locals())
        return await self._get(self.WITHDRAW_NETWORKS_URI, **kwargs)

    async def submit_withdraw(  # type: ignore[override] # noqa: PLR0913
        self,
        symbol: str,
        network_id: int,
        address: str,
        value: str,
        memo: str | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.SubmitWithdrawResponse]:
        """
        Submit a withdrawal.

        Args:
            symbol (str): The symbol
            network_id (int): The network ID.
            address (str): The address.
            value (str): The value.
            memo (str | None): The memo.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        kwargs["data"] = self._get_kwargs_from_locals(locals())
        return await self._post(self.SUBMIT_WITHDRAW_URI, signed=True, **kwargs)

    async def get_deposit_networks(  # type: ignore[override]
        self, symbol: str, **kwargs: Any
    ) -> rt.BaseResponse[rt.DepositNetworksResponse]:
        """
        Get the deposit networks.

        Args:
            symbol (str): The symbol.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        kwargs["params"] = self._get_kwargs_from_locals(locals())
        return await self._get(self.DEPOSIT_NETWORKS_URI, **kwargs)

    async def get_assets_information(  # type: ignore[override]
        self,
        name: str | None = None,
        alphabet: str | None = None,
        without_irt: str | None = None,
        without_zero: str | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.AssetInformationResponse]:
        """
        Get the assets' information.

        Args:
            name (str | None): The name.
            alphabet (str | None): The starting alphabet.
            without_irt (str | enums.WithoutIrt | None): If the IRT should be excluded.
            without_zero (str | enums.WithoutZero | None): If the zero balances should be excluded.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.

        Notes:
            Use `without_irt` and `without_zero` respective enums for better readability.
        """
        kwargs["params"] = self._get_kwargs_from_locals(locals())
        return await self._get(self.ASSETS_INFORMATION_URI, **kwargs)

    async def get_assets_history(  # type: ignore[override]
        self,
        type: str | enums.TransactionType | None = None,  # noqa: A002
        symbol: str | None = None,
        coin_type: str | enums.CoinType | None = None,
        reason_type: str | enums.ReasonType | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.AssetsHistoryResponse]:
        """
        Get the assets' history.

        Args:
            type (str | enums.TransactionType | None): The transaction type.
            symbol (str | None): The symbol.
            coin_type (str | enums.CoinType | None): The coin type.
            reason_type (str | enums.ReasonType | None): The reason type.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.

        Notes:
            Use `type`, `coin_type`, and `reason_type` respective enums for better readability.
        """
        kwargs["params"] = self._get_kwargs_from_locals(locals())
        return await self._get(self.ASSETS_HISTORY_URI, **kwargs)

    async def create_order(  # type: ignore[override] # noqa: PLR0913, PLR0917
        self,
        base_coin_symbol: str,
        quote_coin_symbol: str,
        category_type: str | enums.OrderCategoryType,
        type: str | enums.OrderType,  # noqa: A002
        amount: float | None = None,
        price: float | None = None,
        quote_coin_amount: float | None = None,
        stop_price: float | None = None,
        trigger_price: float | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.CreateOrderResponse]:
        """
        Create an order.

        Args:
            base_coin_symbol (str): The base coin symbol.
            quote_coin_symbol (str): The quote coin symbol.
            category_type (str | enums.OrderCategoryType): The order category type.
            type (str | enums.OrderType): The order type.
            amount (float | None): The amount.
            price (float | None): The price.
            quote_coin_amount (float | None): The quote coin amount.
            stop_price (float | None): The stop price.
            trigger_price (float | None): The trigger price.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.

        Notes:
            Use `category_type` and `type` respective enums for better readability.
        """
        kwargs["data"] = self._get_kwargs_from_locals(locals())
        return await self._post(self.CREATE_ORDER_URI, signed=True, **kwargs)

    async def cancel_order(  # type: ignore[override]
        self, order_id: int, **kwargs: Any
    ) -> rt.BaseResponse[rt.CancelOrderResponse]:
        """
        Cancel an order.

        Args:
            order_id (int): The order ID.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        kwargs["data"] = self._get_kwargs_from_locals(locals())
        return await self._post(self.CANCEL_ORDER_URI, signed=True, **kwargs)

    async def get_orders_history(  # type: ignore[override] # noqa: PLR0913, PLR0917
        self,
        is_trade: str | enums.IsTrade,
        market_id: int | None = None,
        type: str | enums.OrderType | None = None,  # noqa: A002
        category_type: str | enums.OrderCategoryType | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.OrdersHistoryResponse]:
        """
        Get the orders' history.

        Args:
            is_trade (str | enums.IsTrade): If the order is a trade.
            market_id (int | None): The market ID.
            type (str | enums.OrderType | None): The order type.
            category_type (str | enums.OrderCategoryType | None): The order category type.
            from_date (str | None): The start date.
            to_date (str | None): The end date.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.

        Notes:
            Use `is_trade`, `type`, and `category_type` respective enums for better readability.
        """
        kwargs["params"] = self._get_kwargs_from_locals(locals())
        return await self._get(self.ORDERS_HISTORY_URI, **kwargs)

    async def get_markets_information(  # type: ignore[override]
        self, page: int | None = None, **kwargs: Any
    ) -> rt.BaseResponse[rt.MarketListResponse]:
        """
        Get the markets' information.

        Args:
            page (int | None): The page.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        kwargs["params"] = self._get_kwargs_from_locals(locals())
        return await self._get(self.MARKETS_INFORMATION_URI, **kwargs)

    async def get_order_book(  # type: ignore[override]
        self, base_coin: str, quote_coin: str, **kwargs: Any
    ) -> rt.BaseResponse[dict[str, rt.OrderBookResponse]]:
        """
        Get the order book.

        Args:
            base_coin (str): The base coin.
            quote_coin (str): The quote coin.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        kwargs["params"] = self._get_kwargs_from_locals(locals())
        return await self._get(self.ORDER_BOOK_URI, **kwargs)

    async def close_connection(self) -> None:  # type: ignore[override]
        """
        Close the connection.

        Returns:
            None
        """
        await self.session.close()
        await asyncio.sleep(0.250)
        self.loop.stop()
        self.loop.close()
