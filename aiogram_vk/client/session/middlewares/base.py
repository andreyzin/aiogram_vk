from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

from aiogram_vk.methods import Response, VkMethod
from aiogram_vk.methods.base import VkType

if TYPE_CHECKING:
    from ...bot import VkBot


class NextRequestMiddlewareType(Protocol[VkType]):  # pragma: no cover
    async def __call__(
        self,
        bot: "VkBot",
        method: VkMethod[VkType],
    ) -> Response[VkType]:
        ...


class RequestMiddlewareType(Protocol):  # pragma: no cover
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[VkType],
        bot: "VkBot",
        method: VkMethod[VkType],
    ) -> Response[VkType]:
        ...


class BaseRequestMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[VkType],
        bot: "VkBot",
        method: VkMethod[VkType],
    ) -> Response[VkType]:
        """
        Execute middleware

        :param make_request: Wrapped make_request in middlewares chain
        :param bot: bot for request making
        :param method: Request method (Subclass of :class:`aiogram.methods.base.VkMethod`)

        :return: :class:`aiogram.methods.Response`
        """
        pass
