import json
import re
import ssl
from functools import partial
from typing import Awaitable, Callable, List, Optional, Self

import aiohttp
import curl_cffi

from aiogram_vk.client.vk import KATE, VkAPIClient
from aiogram_vk.methods import auth
from aiogram_vk.types import Captcha, CaptchaAnswer
from aiogram_vk.utils import CaptchaSolverProtocol

from ..errors import AuthError, IncorrectPassword
from ..event_pipe import AuthEvent, AuthEventPipeProtocol
from ..scope import UserTokenScope, calculate_user_token_scope_value
from .base import BaseTokenProvider
from .data import AuthCredentials, ConnectAuthorizeCookies
from .utils import generate_device_id


class WebTokenFlow(BaseTokenProvider):

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
        self._event_pipe = event_pipe

    async def get_login_page_credentials(self):
        r = await self._session.get(
            "https://m.vk.ru/join?vkid_auth_type=sign_in",
            headers={
                "cookie": "remixmdevice=1920/1080/1/\u0021\u0021-\u0021\u0021\u0021\u0021\u0021\u0021\u0021\u0021/754",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            },
        )
        res = re.search(r"window\.init\s*=\s*({.*?});", await r.text(), re.DOTALL)
        if not res:
            raise AuthError("Failed to get the value of variable window.init.")

        json_config = res.group(1)
        remixuas = r.cookies["remixuas"]
        return AuthCredentials(
            json.loads(json_config),
            remixuas.value,
            "",
            False,
        )

    async def validate_account(self, auth_credentials: AuthCredentials):
        from aiogram_vk import VkBot

        bot = VkBot(
            access_token="",
            captcha_handler=(
                partial(
                    self._captcha_solver,
                    remixuas=auth_credentials.remixuas,
                )
                if self._captcha_solver
                else None
            ),
        )
        auth_validate = await bot(
            auth.ValidateAccount(
                login=self._login,
                client_id=auth_credentials.page_config["auth"]["host_app_id"],
                device_id=auth_credentials.device_id,
                auth_token=auth_credentials.access_token,
            ).with_cookies({"remixuas": auth_credentials.remixuas}),
            max_captcha_retries=4,
        )
        return auth_validate

    async def act_connect_authorize(
        self, auth_credentials: AuthCredentials, captcha_answer: Optional[CaptchaAnswer] = None
    ) -> ConnectAuthorizeCookies:

        cookies = {
            "remixuas": auth_credentials.remixuas,
        }

        data = {
            "username": f"+{self._login}",
            "password": self._password,
            "auth_token": auth_credentials.access_token,
            "sid": "",
            "uuid": auth_credentials.uuid,
            "v": "5.258",
            "device_id": auth_credentials.device_id,
            "service_group": "",
            "agreement_hash": "",
            "oauth_version": "",
            "max_messenger_hash": "",
            "oauth_force_hash": "0",
            "is_registration": "0",
            "oauth_response_type": "",
            "vkid_oauth_hash": "",
            "is_oauth_migrated_flow": "0",
            "oauth_state": "",
            "to": "aHR0cHM6Ly9tLnZrLnJ1L2xvZ2lu",
            "save_user": "1",
            "version": "1",
            "app_id": auth_credentials.app_id,
        }
        if captcha_answer:
            data["success_token"] = captcha_answer.success_token or ""
            data["captcha_sid"] = str(captcha_answer.captcha_sid or "")
            data["captcha_key"] = captcha_answer.key or ""

        r = await curl_cffi.AsyncSession[curl_cffi.Response]().post(
            "https://login.vk.ru/?act=connect_authorize",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "origin": "https://id.vk.ru",
                "referer": "https://id.vk.ru/",
            },
            data=data,
            cookies=cookies,
            impersonate="chrome",
            http_version="v2",
            default_headers=False,
        )
        if r.json().get("type") == "captcha":
            await self.propagate_event_pipe(
                AuthEvent(
                    name="Meet captcha",
                    description="Trying to solve the captcha automatically",
                )
            )
            if self._captcha_solver is None:
                raise AuthError("Captcha solver is not provided")
            captcha_answer = await self._captcha_solver(
                Captcha(**r.json()),
                remixuas=auth_credentials.remixuas,
            )
            return await self.act_connect_authorize(auth_credentials, captcha_answer)

        if r.json().get("type") == "error":
            raise IncorrectPassword(r.json().get("error_info"))

        return ConnectAuthorizeCookies(
            p=r.cookies["p"],
            remixsid=r.cookies["remixsid"],
        )

    async def act_connect_internal(
        self,
        return_auth_hash: str,
        p: str,
        remixsid: str,
        remixuas: Optional[str] = None,
        captcha_answer: Optional[CaptchaAnswer] = None,
    ):
        data = {
            "uuid": "",
            "service_group": "",
            "device_id": generate_device_id(),
            "oauth_version": "",
            "return_auth_hash": return_auth_hash,
            "version": "1",
            "app_id": "2685278",
        }
        if captcha_answer:
            data["success_token"] = captcha_answer.success_token or ""
            data["captcha_sid"] = str(captcha_answer.captcha_sid or "")
            data["captcha_key"] = captcha_answer.key or ""

        r = await curl_cffi.AsyncSession[curl_cffi.Response]().post(
            "https://login.vk.ru/?act=connect_internal",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "origin": "https://id.vk.ru",
                "referer": "https://id.vk.ru/",
            },
            data=data,
            cookies={"p": p, "remixsid": remixsid},
            impersonate="chrome",
            http_version="v2",
            default_headers=False,
        )
        if r.json().get("type") == "captcha":
            await self.propagate_event_pipe(
                AuthEvent(
                    name="Meet captcha",
                    description="Trying to solve the captcha automatically",
                )
            )
            if self._captcha_solver is None:
                raise AuthError("Captcha solver is not provided")
            captcha_answer = await self._captcha_solver(
                Captcha(**r.json()),
                remixuas=remixuas,
            )
            return await self.act_connect_internal(
                return_auth_hash, p, remixsid, remixuas, captcha_answer
            )
        return r.json()

    async def authorize_client(self, remixsid: str) -> dict:
        r = await self._session.get(
            f"https://oauth.vk.com/authorize?client_id={self._vk_api_client.client_id}&scope={calculate_user_token_scope_value(self._scope)}&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1",
            cookies={"remixsid": remixsid},
            headers={
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            },
        )
        result = re.search(r"window\.init = ({.*?});", await r.text(), re.DOTALL)
        assert result
        data = json.loads(result.group(1))
        return data

    async def get_oauth_token(self, hash: str, auth_user_hash: str, access_token: str) -> str:
        from aiogram_vk import VkBot

        bot = VkBot(
            access_token="",
            captcha_handler=self._captcha_solver,
        )
        oauth_token = await bot(
            auth.GetOauthToken(
                # hash=data["data"]["hash"]["return_auth"],
                hash=hash,
                # auth_user_hash=data['data']['hash']['return_auth'],
                auth_user_hash=auth_user_hash,
                app_id=self._vk_api_client.client_id,
                scope=1040183263,
                client_id=KATE.client_id,
                access_token=access_token,
                is_seamless_auth=1,
            ),
            max_captcha_retries=4,
        )
        return oauth_token.access_token

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
            credentials = await self.get_login_page_credentials()
            await self.propagate_event_pipe(
                AuthEvent(
                    name="Got credentials",
                    description="Scraped tokens from the login page",
                )
            )
            validated = await self.validate_account(credentials)
            await self.propagate_event_pipe(
                AuthEvent(
                    name="Validated auth account",
                    description="Got available auth flow methods but they are not supported yet",
                )
            )
            connect_authorize = await self.act_connect_authorize(credentials)
            await self.propagate_event_pipe(
                AuthEvent(
                    name="Sent connect authorize request",
                    description="Web auth processed",
                )
            )
            authorize_client = await self.authorize_client(connect_authorize.remixsid)
            await self.propagate_event_pipe(
                AuthEvent(
                    name="Authorized client",
                    description="Got data for requested client",
                )
            )
            connect_internal = await self.act_connect_internal(
                return_auth_hash=authorize_client["data"]["hash"]["return_auth"],
                p=connect_authorize.p,
                remixsid=connect_authorize.remixsid,
                remixuas=credentials.remixuas,
            )
            await self.propagate_event_pipe(
                AuthEvent(
                    name="Obtained connect hash",
                    description="Got connect internal data",
                )
            )
            self._token = await self.get_oauth_token(
                hash=authorize_client["data"]["hash"]["return_auth"],
                auth_user_hash=connect_internal["data"]["auth_user_hash"],
                access_token=connect_internal["data"]["access_token"],
            )
            if self._token is None:
                raise AuthError("Invalid client or credentials")

        await self.propagate_event_pipe(
            AuthEvent(
                name="Got oauth token",
                description="Flow completed successfully",
            )
        )
        return self._token

    async def propagate_event_pipe(self, event: AuthEvent) -> None:
        if self._event_pipe:
            await self._event_pipe(event)
