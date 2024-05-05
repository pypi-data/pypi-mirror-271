"""
# Enums

Enum classes for the Bit24 API.

## Enums

- `HTTPMethod`: HTTP methods.
- `WithoutIrt`: Without IRT.
- `WithoutZero`: Without zero.
- `TransactionType`: Transaction type.
- `CoinType`: Coin type.
- `ReasonType`: Reason type.
- `BalanceStatus`: Balance status.
- `OrderType`: Order type.
- `OrderCategoryType`: Order category type.
- `OrderStatus`: Order status.
- `IsTrade`: Is trade.
"""

try:
    from enum import StrEnum  # type: ignore[attr-defined] # noqa: RUF100
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):  # type: ignore[no-redef] # noqa: UP042
        """Enum class for older Python versions"""

        def __str__(self) -> str:
            """
            String representation.

            Returns:
                str: The string representation.
            """
            return str(self.value)

        def __repr__(self) -> str:
            """
            Representation.

            Returns:
                str: The representation.
            """
            return str(self.value)


class HTTPMethod(StrEnum):
    """
    HTTP methods.

    Attributes:
        GET (str): GET.
        POST (str): POST.
        PUT (str): PUT.
        DELETE (str): DELETE.
        PATCH (str): PATCH.

    Examples:
        >>> HTTPMethod.GET
        'GET'

        >>> HTTPMethod.POST
        'POST'

        >>> HTTPMethod.PUT
        'PUT'

        >>> HTTPMethod.DELETE
        'DELETE'

        >>> HTTPMethod.PATCH
        'PATCH'
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class WithoutIrt(StrEnum):
    """
    Without IRT.

    Attributes:
        ALL (str): All.
        WITHOUT_IRT (str): Without IRT.

    Examples:
        >>> WithoutIrt.ALL
        0

        >>> WithoutIrt.WITHOUT_IRT
        1
    """

    ALL = "0"
    WITHOUT_IRT = "1"


class WithoutZero(StrEnum):
    """
    Without zero.

    Attributes:
        ALL (str): All.
        WITHOUT_ZERO (str): Without zero.

    Examples:
        >>> WithoutZero.ALL
        0

        >>> WithoutZero.WITHOUT_ZERO
        1
    """

    ALL = "0"
    WITHOUT_ZERO = "1"


class TransactionType(StrEnum):
    """
    Transaction type.

    Attributes:
        DECREASING (str): Decreasing.
        INCREASING (str): Increasing.

    Examples:
        >>> TransactionType.DECREASING
        0

        >>> TransactionType.INCREASING
        1
    """

    DECREASING = "0"
    INCREASING = "1"


class CoinType(StrEnum):
    """
    Coin type.

    Attributes:
        CRYPTO (str): Crypto.
        FIAT (str): Fiat.

    Examples:
        >>> CoinType.CRYPTO
        0

        >>> CoinType.FIAT
        1
    """

    CRYPTO = "0"
    FIAT = "1"


class ReasonType(StrEnum):
    """
    Reason type.

    Attributes:
        DEPOSIT (str): Deposit.
        WITHDRAWAL (str): Withdrawal.
        PROFESSIONAL_TRADING (str): Professional trading.
        PROFESSIONAL_TRADING_REFERRAL_COMMISSION (str): Professional trading referral commission.
        INSTANT_TRADING (str): Instant trading.
        SUPPORT (str): Support.
        DEPOSIT_WITH_PAYMENT_ID (str): Deposit with payment ID.
        GIFT_CODE (str): Gift code.
        INSTANT_TRADING_REFERRAL_COMMISSION (str): Instant trading referral commission.
        REFERRAL_COMMISSION (str): Referral commission.
        SMALL_ASSET_TRADING (str): Small asset trading.

    Examples:
        >>> ReasonType.DEPOSIT
        0

        >>> ReasonType.WITHDRAWAL
        1

        >>> ReasonType.PROFESSIONAL_TRADING
        2

        >>> ReasonType.PROFESSIONAL_TRADING_REFERRAL_COMMISSION
        3

        >>> ReasonType.INSTANT_TRADING
        6

        >>> ReasonType.SUPPORT
        7

        >>> ReasonType.DEPOSIT_WITH_PAYMENT_ID
        8

        >>> ReasonType.GIFT_CODE
        9

        >>> ReasonType.INSTANT_TRADING_REFERRAL_COMMISSION
        10

        >>> ReasonType.REFERRAL_COMMISSION
        11

        >>> ReasonType.SMALL_ASSET_TRADING
        12
    """

    DEPOSIT = "0"
    WITHDRAWAL = "1"
    PROFESSIONAL_TRADING = "2"
    PROFESSIONAL_TRADING_REFERRAL_COMMISSION = "3"
    INSTANT_TRADING = "6"
    SUPPORT = "7"
    DEPOSIT_WITH_PAYMENT_ID = "8"
    GIFT_CODE = "9"
    INSTANT_TRADING_REFERRAL_COMMISSION = "10"
    REFERRAL_COMMISSION = "11"
    SMALL_ASSET_TRADING = "12"


class BalanceStatus(StrEnum):
    """
    Balance status.

    Attributes:
        IN_PROGRESS (str): In progress.
        COMPLETED (str): Completed.

    Examples:
        >>> BalanceStatus.IN_PROGRESS
        0

        >>> BalanceStatus.COMPLETED
        1
    """

    IN_PROGRESS = "0"
    COMPLETED = "1"


class OrderType(StrEnum):
    """
    Order type.

    Attributes:
        SELL: Sell.
        BUY: Buy.

    Examples:
        >>> OrderType.SELL
        0

        >>> OrderType.BUY
        1
    """

    SELL = "0"
    BUY = "1"


class OrderCategoryType(StrEnum):
    """
    Order category type.

    Attributes:
        LIMIT (str): Limit.
        MARKET (str): Market.
        STOP_LIMIT_OR_STOP_MARKET (str): Stop limit or stop market.
        OCO (str): OCO.

    Examples:
        >>> OrderCategoryType.LIMIT
        0

        >>> OrderCategoryType.MARKET
        1

        >>> OrderCategoryType.STOP_LIMIT_OR_STOP_MARKET
        2

        >>> OrderCategoryType.OCO
        3
    """

    LIMIT = "0"
    MARKET = "1"
    STOP_LIMIT_OR_STOP_MARKET = "2"
    OCO = "3"


class OrderStatus(StrEnum):
    """
    Order status.

    Attributes:
        OPEN (str): Open.
        DONE_OR_CANCELLED (str): Done or cancelled.

    Examples:
        >>> OrderStatus.OPEN
        0

        >>> OrderStatus.DONE_OR_CANCELLED
        1
    """

    OPEN = "0"
    DONE_OR_CANCELLED = "1"


class IsTrade(StrEnum):
    """
    Is trade.

    Attributes:
        ORDER (str): Order.
        TRADE (str): Trade.

    Examples:
        >>> IsTrade.ORDER
        0

        >>> IsTrade.TRADE
        1
    """

    ORDER = "0"
    TRADE = "1"
