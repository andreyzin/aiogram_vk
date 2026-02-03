from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field, field_serializer

from aiogram_vk.types import AuthValidateAccountResult

from ..base import VkMethod


class ValidateAccount(VkMethod[AuthValidateAccountResult]):
    """
    Validate account
    """

    __returning__ = AuthValidateAccountResult
    __api_method__ = "auth.validateAccount"

    login: str
    client_id: int
    device_id: str
    supported_ways: list[str] = Field(
        default_factory=lambda: "push,email,qr_code,codegen,sms,callreset,password,reserve_code,max_messenger,official_messenger,passkey".split(
            ","
        )
    )

    @field_serializer("supported_ways")
    def serialize_supported_ways(self, supported_ways: list[str]) -> str:
        return ",".join(supported_ways)

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            login: str,
            client_id: int,
            device_id: str,
            supported_ways: list[str] = [
                "push",
                "email",
                "qr_code",
                "codegen",
                "sms",
                "callreset",
                "password",
                "reserve_code",
                "max_messenger",
                "official_messenger",
                "passkey",
            ],
            **__pydantic_kwargs: Any,
        ) -> None:
            ...
            # super().__init__(
            #     login=login,
            #     client_id=client_id,
            #     device_id=device_id,
            #     supported_ways=supported_ways,
            #     **__pydantic_kwargs,
            # )
