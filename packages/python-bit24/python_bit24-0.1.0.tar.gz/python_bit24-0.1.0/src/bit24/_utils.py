"""
# Utils

This module contains utility functions.

## Functions
- `get_loop`: Get event loop.
"""

import asyncio


def get_loop() -> asyncio.AbstractEventLoop:
    """
    Get event loop.

    Returns:
        asyncio.AbstractEventLoop: The event loop.

    Examples:
        >>> get_loop()
        <_UnixSelectorEventLoop running=True closed=False debug=False>
    """
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith("There is no current event loop in thread"):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        raise
