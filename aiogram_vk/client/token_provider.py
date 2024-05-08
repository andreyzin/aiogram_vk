from enum import Enum
from typing import Awaitable, Callable, List, Optional, Self, Union

import aiohttp
from pydantic import BaseModel

from aiogram_vk.client.vk import KATE, VkAPIClient


class UserTokenScope(str, Enum):
    notify = "notify"
    "The user allowed to send him notifications (for flash/iframe applications)"
    friends = "friends"
    "Access to friends."
    photos = "photos"
    "Access to photos."
    audio = "audio"
    "Access to audio recordings."
    video = "video"
    "Access to video."
    stories = "stories"
    "Access to stories"
    pages = "pages"
    "Access to wiki pages"
    menu = "menu"
    "Add a link to the application in the menu on the left."
    status = "status"
    "Access to user status."
    notes = "notes"
    "Access to user notes."
    messages = "messages"
    "Access to advanced methods of working with messages (only for Standalone applications, past moderation )."
    wall = "wall"
    """Access to conventional and advanced methods of working with the wall. This right of access by default is not available for sites (ignored when trying to authorize for applications with the type "Website" or according to the scheme Authorization Code Flow )."""
    ads = "ads"
    "Access to advanced methods of working with the advertising API . Available for authorization according to the scheme Implicit Flow or Authorization Code Flow ."
    offline = "offline"
    "Access to API at any time (when using this option, the parameter expires_in returned with access_token contains 0 — an infinite token). It is not used in Open API."
    docs = "docs"
    "Access to documents."
    groups = "groups"
    "Access to user groups."
    notifications = "notifications"
    "Access to user response alerts."
    stats = "stats"
    "Access to statistics of groups and applications of the user, the administrator of which he is."
    email = "email"
    "Access to the user's email."
    market = "market"
    "Access to goods."
    phone_number = "phone_number"
    "Access to phone number."


class VkError(Exception):
    pass


class AuthError(VkError):
    pass


class CaptchaError(AuthError):
    pass


class Need2FAError(AuthError):
    pass


class InvalidClient(AuthError):
    pass


class Captcha(BaseModel):
    sid: int
    img: str
    key: Optional[str] = None


class VkTokenProvider:

    def __init__(
        self,
        login: str,
        password: str,
        scope: List[UserTokenScope] = [UserTokenScope.offline, UserTokenScope.audio],
        vk_api_client: VkAPIClient = KATE,
        session: Optional[aiohttp.ClientSession] = None,
        captcha_solver: Optional[Callable[[Captcha], Awaitable[str]]] = None,
        two_factor_auth: Optional[Callable[[Self], Awaitable[str]]] = None,
        api_version: str = "5.131",
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
        self._session = session or aiohttp.ClientSession()
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
            print(auth_response)
            error = auth_response["error"]
            if error == "need_captcha":
                if self._captcha_solver is None:
                    raise CaptchaError("Captcha solver is not set")

                captcha = Captcha(
                    sid=auth_response["captcha_sid"],
                    img=auth_response["captcha_img"],
                )
                captcha.key = await self._captcha_solver(captcha)
                auth_response = await self.send_auth(captcha=captcha)

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
        captcha: Optional[Captcha] = None,
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

        if captcha:
            if captcha.key is None:
                raise CaptchaError("Captcha key is not set")

            params["captcha_sid"] = captcha.sid
            params["captcha_key"] = captcha.key

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
