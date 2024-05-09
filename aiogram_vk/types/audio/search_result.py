from __future__ import annotations

from typing import List

from ..base import VkObject
from .audio import Audio


class AudioSearchResult(VkObject):
    """
    Audio search result
    """

    count: int
    "Number of results"
    items: List[Audio]
    "List of results"
