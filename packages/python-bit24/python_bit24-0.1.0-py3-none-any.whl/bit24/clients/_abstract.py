"""
# Abstract Client

This module contains the abstract client class that is used by the main client class.
"""

from abc import ABC, abstractmethod
from typing import Any

from .. import enums
from .. import types as t
from ..types import responses as rt
from ._core import CoreClient


class AbstractClient(ABC):
    """
    Abstract client class that contains the abstract methods that the main client class should implement.

    Methods:
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
    """

    @abstractmethod
    def _init_session(self) -> t.HttpSession:
        """
        (Abstract, Private)

        Initialize the session.

        Returns:
            requests.Session: The session.
        """
        raise NotImplementedError

    @abstractmethod
    def _request(
        self, method: enums.HTTPMethod, uri: str, signed: bool = False, **kwargs: Any
    ) -> rt.BaseResponse:
        """
        (Abstract, Private)

        Make a request.

        Args:
            method (HTTPMethod): The HTTP method.
            uri (str): The URI.
            signed (bool): If the request is signed.
            **kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def _request_api(
        self,
        method: enums.HTTPMethod,
        path: str,
        signed: bool = False,
        version: str = CoreClient.API_VERSION,
        **kwargs: Any,
    ) -> rt.BaseResponse:
        """
        (Abstract, Private)

        Make a request to the API.

        Args:
            method (HTTPMethod): The HTTP method.
            path (str): The path.
            signed (bool): If the request is signed.
            version (str): The API version.
            **kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def _get(
        self,
        path: str,
        signed: bool = False,
        version: str = CoreClient.API_VERSION,
        **kwargs: Any,
    ) -> rt.BaseResponse:
        """
        (Abstract, Private)

        Make a GET request to the API.

        Args:
            path (str): The path.
            signed (bool): If the request is signed.
            version (str): The API version.
            **kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def _post(
        self,
        path: str,
        signed: bool = False,
        version: str = CoreClient.API_VERSION,
        **kwargs: Any,
    ) -> rt.BaseResponse:
        """
        (Abstract, Private)

        Make a POST request to the API.

        Args:
            path (str): The path.
            signed (bool): If the request is signed.
            version (str): The API version.
            **kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _handle_response(response: t.HttpResponse) -> rt.BaseResponse:
        """
        (Abstract, Private)

        Handle the response.

        Args:
            response (HttpResponse): The response.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def get_withdraw_networks(
        self, symbol: str, **kwargs: Any
    ) -> rt.BaseResponse[rt.WithdrawalNetworksResponse]:
        """
        (Abstract)

        Get the withdrawal networks.

        Args:
            symbol (str): The symbol.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def submit_withdraw(  # noqa: PLR0913
        self,
        symbol: str,
        network_id: int,
        address: str,
        value: str,
        memo: str | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.SubmitWithdrawResponse]:
        """
        (Abstract)

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
        raise NotImplementedError

    @abstractmethod
    def get_deposit_networks(
        self, symbol: str, **kwargs: Any
    ) -> rt.BaseResponse[rt.DepositNetworksResponse]:
        """
        (Abstract)

        Get the deposit networks.

        Args:
            symbol (str): The symbol.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def get_assets_information(
        self,
        name: str | None = None,
        alphabet: str | None = None,
        without_irt: str | None = None,
        without_zero: str | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.AssetInformationResponse]:
        """
        (Abstract)

        Get the assets' information.

        Args:
            name (str | None): The name.
            alphabet (str | None): The starting alphabet.
            without_irt (str | enums.WithoutIrt | None): If the IRT should be excluded.
            without_zero (str | enums.WithoutZero | None): If the zero balances should be excluded.
            kwargs: The keyword arguments.

        Returns:
            rt.BaseResponse: The response.

        Notes:
            Use `without_irt` and `without_zero` respective enums for better readability.
        """
        raise NotImplementedError

    @abstractmethod
    def get_assets_history(
        self,
        type: str | enums.TransactionType | None = None,  # noqa: A002
        symbol: str | None = None,
        coin_type: str | enums.CoinType | None = None,
        reason_type: str | enums.ReasonType | None = None,
        **kwargs: Any,
    ) -> rt.BaseResponse[rt.AssetsHistoryResponse]:
        """
        (Abstract)

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
        raise NotImplementedError

    @abstractmethod
    def create_order(  # noqa: PLR0913, PLR0917
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
        (Abstract)

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
        raise NotImplementedError

    @abstractmethod
    def cancel_order(
        self, order_id: int, **kwargs: Any
    ) -> rt.BaseResponse[rt.CancelOrderResponse]:
        """
        (Abstract)

        Cancel an order.

        Args:
            order_id (int): The order ID.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def get_orders_history(  # noqa: PLR0913, PLR0917
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
        (Abstract)

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
        raise NotImplementedError

    @abstractmethod
    def get_markets_information(
        self, page: int | None = None, **kwargs: Any
    ) -> rt.BaseResponse[rt.MarketListResponse]:
        """
        (Abstract)

        Get the markets' information.

        Args:
            page (int | None): The page.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def get_order_book(
        self, base_coin: str, quote_coin: str, **kwargs: Any
    ) -> rt.BaseResponse[dict[str, rt.OrderBookResponse]]:
        """
        (Abstract)

        Get the order book.

        Args:
            base_coin (str): The base coin.
            quote_coin (str): The quote coin.
            kwargs (Any): The keyword arguments.

        Returns:
            rt.BaseResponse: The response.
        """
        raise NotImplementedError

    @abstractmethod
    def close_connection(self) -> None:
        """
        (Abstract)

        Close the connection.
        """
        raise NotImplementedError
