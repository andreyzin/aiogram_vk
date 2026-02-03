from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from aiogram_vk.types import VkObject

from ..base import VkMethod


class Force(VkMethod[VkObject]):
    """
    Returns amount of user or community audios.
    """

    __returning__ = VkObject
    __api_method__ = "captcha.force"


    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                **__pydantic_kwargs,
            )
