from typing import Awaitable, Callable, List, Optional, Self

import aiohttp

from aiogram_vk.client.vk import KATE, VkAPIClient
from aiogram_vk.utils import CaptchaSolverProtocol

from ..event_pipe import AuthEvent, AuthEventPipeProtocol
from ..scope import UserTokenScope


class BaseTokenProvider:
    _login: str
    _password: str
    _scope: List[UserTokenScope]
    _vk_api_client: VkAPIClient
    _session: aiohttp.ClientSession
    _captcha_solver: Optional[CaptchaSolverProtocol]
    _two_factor_auth: Optional[Callable[[Self], Awaitable[str]]]
    _api_version: str
    _event_pipe: Optional[AuthEventPipeProtocol]

    def __init__(
        self,
        login: str,
        password: str,
        scope: List[UserTokenScope] = [UserTokenScope.offline, UserTokenScope.audio],
        vk_api_client: VkAPIClient = KATE,
        session: Optional[aiohttp.ClientSession] = None,
        captcha_solver: Optional[CaptchaSolverProtocol] = None,
        two_factor_auth: Optional[Callable[[Self], Awaitable[str]]] = None,
        api_version: str = "5.258",
        event_pipe: Optional[AuthEventPipeProtocol] = None,
    ):
        raise NotImplementedError()

    async def get_token(self) -> str:
        """
        Asynchronously retrieves the access token.

        This method checks if the access token is already available. If not, it calls the `auth` method to perform the authorization process. If the authorization is successful, the access token is stored and returned. If the authorization fails or the access token is still not available, an `AuthError` is raised.

        Returns:
            str: The access token.

        Raises:
            AuthError: If the access token is invalid or not available.
        """

        raise NotImplementedError()

    async def propagate_event_pipe(self, event: AuthEvent) -> None:
        if self._event_pipe:
            await self._event_pipe(event)
