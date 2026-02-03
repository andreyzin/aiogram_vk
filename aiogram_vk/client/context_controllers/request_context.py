from typing import Optional

from pydantic import BaseModel, PrivateAttr
from typing_extensions import Self


class RequestContextController(BaseModel):
    _cookies: Optional["dict[str, str]"] = PrivateAttr(default_factory=dict)

    def with_cookies(self, cookies: dict[str, str], override: bool = True) -> Self:
        """
        Add cookies to request

        :param cookies: Cookies
        :param override: Override existing cookies
        :return: self
        """
        if override:
            self._cookies = cookies
        else:
            self._cookies = self._cookies or {}
            self._cookies.update(cookies)
        return self

    @property
    def cookies(self) -> Optional["dict[str, str]"]:
        """
        Get cookies

        :return: Cookies
        """
        return self._cookies
