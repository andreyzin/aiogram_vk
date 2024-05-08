from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...types import AccountInfo
from ..base import VkMethod


class GetInfo(VkMethod[AccountInfo]):
    """
    Returns current account info.

    Source: https://dev.vk.com/ru/method/account.getInfo
    """

    __returning__ = AccountInfo
    __api_method__ = "account.getInfo"

    
    if TYPE_CHECKING:

        def __init__(__pydantic__self__, **__pydantic_kwargs: Any) -> None:
            super().__init__(**__pydantic_kwargs)
