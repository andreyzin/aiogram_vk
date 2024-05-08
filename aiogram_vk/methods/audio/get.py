from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from aiogram_vk.types.base import VkObject

from ..base import VkMethod


class Get(VkMethod[VkObject]):
    """
    Returns amount of user or community audios.
    """

    __returning__ = VkObject
    __api_method__ = "audio.get"

    owner_id: int
    "ID of the user or community that owns the audio album(s). Use a negative value to designate a community ID."
    playlist_id: Optional[int] = None
    "ID of the audio playlist, if needed"
    offset: Optional[int] = 0
    "Offset needed to return a specific subset of audios"

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            owner_id: int,
            playlist_id: Optional[int] = None,
            offset: Optional[int] = 0,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                owner_id=owner_id,
                playlist_id=playlist_id,
                offset=offset,
                **__pydantic_kwargs,
            )
