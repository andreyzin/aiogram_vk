from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..base import VkMethod


class GetCount(VkMethod[int]):
    """
    Returns amount of user or community audios.
    """

    __returning__ = int
    __api_method__ = "audio.getCount"

    owner_id: int
    "ID of the user or community that owns the audio album(s). Use a negative value to designate a community ID."

    if TYPE_CHECKING:

        def __init__(__pydantic__self__, *, owner_id: int, **__pydantic_kwargs: Any) -> None:
            super().__init__(owner_id=owner_id, **__pydantic_kwargs)
