"""
# Bit24 Python SDK

An unofficial Python SDK for the [Bit24 API](https://docs.bit24.cash)
"""

__author__ = "AMiWR"
__version__ = "0.1.0"
__license__ = "MIT"
__email__ = "amiwrpremium@gmail.com"
__url__ = "https://github.com/amiwrpremium/python-bit24"
__description__ = "An unofficial Python SDK for the Bit24 API"

__all__ = ["AsyncClient", "Client"]

from .clients import AsyncClient, Client
