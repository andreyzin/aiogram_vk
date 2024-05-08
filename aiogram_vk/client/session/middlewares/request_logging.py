import logging
from typing import TYPE_CHECKING, Any, List, Optional, Type

from aiogram_vk import loggers
from aiogram_vk.methods import VkMethod
from aiogram_vk.methods.base import Response, VkType

from .base import BaseRequestMiddleware, NextRequestMiddlewareType

if TYPE_CHECKING:
    from ...bot import VkBot

logger = logging.getLogger(__name__)


class RequestLogging(BaseRequestMiddleware):
    def __init__(self, ignore_methods: Optional[List[Type[VkMethod[Any]]]] = None):
        """
        Middleware for logging outgoing requests

        :param ignore_methods: methods to ignore in logging middleware
        """
        self.ignore_methods = ignore_methods if ignore_methods else []

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[VkType],
        bot: "VkBot",
        method: VkMethod[VkType],
    ) -> Response[VkType]:
        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                "Make request with method=%r by bot id=%d",
                type(method).__name__,
                bot.id,
            )
        return await make_request(bot, method)
