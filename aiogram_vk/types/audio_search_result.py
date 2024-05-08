from __future__ import annotations

from typing import List


from aiogram_vk.types.audio import Audio

from .base import VkObject


class AudioSearchResult(VkObject):
    """
    Audio search result
    """

    count: int
    "Number of results"
    items: List[Audio]
    "List of results"
