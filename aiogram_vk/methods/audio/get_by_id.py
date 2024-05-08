from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from pydantic import field_serializer

from aiogram_vk.types.audio import Audio

from ..base import VkMethod


class GetById(VkMethod[List[Audio]]):
    """
    Returns audios by their IDs.
    """

    __returning__ = List[Audio]
    __api_method__ = "audio.getById"

    audios: List[str]
    """IDs of audios to get information about. Sample "{owner_id}_{audio_id}"."""

    @field_serializer("audios")
    def serialize_audios(self, audios: List[str]) -> str:
        return ",".join(audios)

    if TYPE_CHECKING:

        def __init__(__pydantic__self__, *, audios: List[str], **__pydantic_kwargs: Any) -> None:
            super().__init__(audios=audios, **__pydantic_kwargs)
