import ssl
from typing import Awaitable, Callable, List, Optional, Self, Union

import aiohttp

from aiogram_vk.client.auth.event_pipe import AuthEventPipeProtocol
from aiogram_vk.client.vk import KATE, VkAPIClient
from aiogram_vk.types.captcha import Captcha, CaptchaAnswer
from aiogram_vk.utils import CaptchaSolverProtocol

from ..errors import AuthError, CaptchaError, InvalidClient, Need2FAError
from ..scope import UserTokenScope
from .base import BaseTokenProvider


class VkTokenProvider(BaseTokenProvider):

    def __init__(
        self,
        login: str,
        password: str,
        scope: List[UserTokenScope] = [UserTokenScope.offline, UserTokenScope.audio],
        vk_api_client: VkAPIClient = KATE,
        session: Optional[aiohttp.ClientSession] = None,
        captcha_solver: Optional[CaptchaSolverProtocol] = None,
        two_factor_auth: Optional[Callable[[Self], Awaitable[str]]] = None,
        api_version: str = "5.131",
        event_pipe: Optional[AuthEventPipeProtocol] = None,
    ):
        """
        Initializes the VkTokenProvider with the provided login, password, and optional parameters.

        Args:
            login (str): The user's login credentials.
            password (str): The user's password.
            vk_api_client (VkAPIClient, optional): The client app to use for VK (default is KateMobile).
            captcha_solver (Optional[Callable[[Captcha], Awaitable[str]], optional): The callable function for solving captchas (default is None).
            two_factor_auth (Optional[Callable[[Self], Awaitable[str]], optional): The callable function for two-factor authentication (default is None).

        Returns:
            None
        """
        self._login = login
        self._password = password
        self._scope = scope
        self._vk_api_client = vk_api_client
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        self._session = session or aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_ctx)
        )
        self._captcha_solver = captcha_solver
        self._two_factor_auth = two_factor_auth
        self.api_version = api_version
        self._token = None

    async def get_token(self) -> str:
        """
        Asynchronously retrieves the access token.

        This method checks if the access token is already available. If not, it calls the `auth` method to perform the authorization process. If the authorization is successful, the access token is stored and returned. If the authorization fails or the access token is still not available, an `AuthError` is raised.

        Returns:
            str: The access token.

        Raises:
            AuthError: If the access token is invalid or not available.
        """
        if self._token is None:
            await self.auth()
            if self._token is None:
                raise AuthError("Invalid client or credentials")

        return self._token

    async def auth(self) -> Union[Self, bool]:
        """
        Performs authorization using the available login and password.
        If necessary, interactively accepts a code from SMS or captcha.

        Returns:
            self: If authorization was successful, returns self.
            False: If authorization was not successful, returns false.
        """
        auth_response = await self.send_auth()
        while "error" in auth_response:
            error = auth_response["error"]
            if error == "need_captcha":
                if self._captcha_solver is None:
                    raise CaptchaError("Captcha solver is not set")

                captcha = Captcha.model_validate(auth_response)
                captcha_answer = await self._captcha_solver(captcha)
                auth_response = await self.send_auth(captcha_answer=captcha_answer)

            elif error == "need_validation":
                if self._two_factor_auth is None:
                    raise Need2FAError("2FA handler is not set")

                await self.validate_phone(auth_response["validation_sid"])
                code: str = await self._two_factor_auth(self)
                auth_response = await self.send_auth(code=code)

            elif error == "invalid_request":
                if self._two_factor_auth is None:
                    raise Need2FAError("2FA handler is not set")

                await self.validate_phone(auth_response["validation_sid"])
                code: str = await self._two_factor_auth(self)
                auth_response = await self.send_auth(code=code)

            elif error == "invalid_client":
                raise InvalidClient()

            else:
                raise Exception(f"Unknown error: {error}")

        if "access_token" in auth_response:
            access_token = auth_response["access_token"]
            self._token = access_token
            return self

        return False

    async def send_auth(
        self,
        code: Optional[str] = None,
        captcha_answer: Optional[CaptchaAnswer] = None,
    ) -> dict:
        """
        Request auth from VK.

        Args:
            code (Optional[str]): Code from VK/SMS (default value = None).
            captcha (Optional[Captcha]): Captcha with key (default value = None).

        Returns:
            Response: Response from VK.
        """
        params = {
            "grant_type": "password",
            "client_id": self._vk_api_client.client_id,
            "client_secret": self._vk_api_client.client_secret,
            "username": self._login,
            "password": self._password,
            "scope": "audio,offline",
            "2fa_supported": 1,
            "force_sms": 1,
            "v": self.api_version,
        }

        if captcha_answer:
            # if captcha.key is None:
            #     raise CaptchaError("Captcha key is not set")
            params = params | captcha_answer.model_dump(exclude_none=True)
            # params["captcha_sid"] = captcha_answer.captcha_sid
            # if captcha_answer.key:
            #     params["captcha_key"] = captcha_answer.key
            # params["success_token"] = captcha_answer.success_token

        if code:
            params["code"] = code

        r = await self._session.post(
            "https://oauth.vk.com/token",
            params=params,
            headers={"User-Agent": self._vk_api_client.user_agent},
        )

        return await r.json()

    async def validate_phone(self, sid: Union[str, int]):
        """
        Request code from VK.

        Args:
            sid (Union[str, int]): Sid from VK.

        Returns:
            Response: Response from VK.
        """
        r = await self._session.post(
            "https://api.vk.com/method/auth.validatePhone",
            params={
                "sid": str(sid),
                "v": self.api_version,
            },
            headers={"User-Agent": self._vk_api_client.user_agent},
        )
        return r.json()
