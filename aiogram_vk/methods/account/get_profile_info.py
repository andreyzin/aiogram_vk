from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...types import AccountUserSettings
from ..base import VkMethod


class GetProfileInfo(VkMethod[AccountUserSettings]):
    """
    Returns current account info.

    Source: https://dev.vk.com/ru/method/account.getProfileInfo
    """

    __returning__ = AccountUserSettings
    __api_method__ = "account.getProfileInfo"

    
    if TYPE_CHECKING:

        def __init__(__pydantic__self__, **__pydantic_kwargs: Any) -> None:
            super().__init__(**__pydantic_kwargs)
