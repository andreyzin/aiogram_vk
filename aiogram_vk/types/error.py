from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .base import VkObject


class Error(VkObject):

    error_code: Optional[int] = None
    error_msg: Optional[str] = None
    request_params: Optional[List[Dict[str, Any]]] = None