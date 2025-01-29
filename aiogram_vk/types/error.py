from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import VkObject


class Error(VkObject):

    error_code: Optional[int] = None
    error_msg: Optional[str] = None
    request_params: Optional[List[Dict[str, Any]]] = None

class CaptchaError(Error):

    captcha_sid: str
    captcha_img: str
    captcha_track: Optional[str] = None