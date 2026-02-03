from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field, field_serializer

from aiogram_vk.types import GetOauthTokenResult

from ..base import VkMethod


class GetOauthToken(VkMethod[GetOauthTokenResult]):
    """
    Get OAuth token
    """

    __returning__ = GetOauthTokenResult
    __api_method__ = "auth.getOauthToken"

    hash: str
    auth_user_hash: str
    app_id: int
    client_id: int
    scope: int
    access_token: str
    is_seamless_auth: int = 1
    

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            hash: str,
            auth_user_hash: str,
            app_id: int,
            client_id: int,
            scope: int,
            access_token: str,
            is_seamless_auth: int = 1,
            **__pydantic_kwargs: Any,
        ) -> None:
            ...
            # super().__init__(
            #     hash=hash,
            #     auth_user_hash=auth_user_hash,
            #     **__pydantic_kwargs,
            # )
