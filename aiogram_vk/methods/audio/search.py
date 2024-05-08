from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional

from aiogram_vk.types.audio_search_result import AudioSearchResult

from ..base import VkMethod


class Search(VkMethod[AudioSearchResult]):
    """
    Returns amount of user or community audios.
    """

    __returning__ = AudioSearchResult
    __api_method__ = "audio.search"

    q: str
    "Search query string"
    offset: Optional[int] = 0
    "Offset needed to return a specific subset of audios"
    count: int = 100
    "Number of audios to return"
    sort: Optional[int] = 0
    "Sort order: '1' — by date added, '0' — by rating"
    autocomplete: Optional[int] = 1
    "Whether to return search suggestions or not"

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            q: str,
            offset: Optional[int] = 0,
            count: int = 100,
            sort: Optional[int] = 0,
            autocomplete: Optional[int] = 1,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                q=q,
                offset=offset,
                count=count,
                sort=sort,
                autocomplete=autocomplete,
                **__pydantic_kwargs,
            )
