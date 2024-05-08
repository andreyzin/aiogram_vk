import asyncio as _asyncio
from contextlib import suppress

from . import enums, methods, types
from .__meta__ import __api_version__, __version__
from .client import session
from .client.bot import VkBot
from .client.token_provider import VkTokenProvider

with suppress(ImportError):
    import uvloop as _uvloop  # type: ignore

    _asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())


__all__ = (
    "__api_version__",
    "__version__",
    "types",
    "methods",
    "enums",
    "VkBot",
    "session",
    "VkTokenProvider",
)
