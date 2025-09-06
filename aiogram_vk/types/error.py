from __future__ import annotations

from typing import Any, Dict, List, Optional

from .captcha import Captcha

from .base import VkObject


class Error(VkObject):

    error_code: Optional[int] = None
    error_msg: Optional[str] = None
    request_params: Optional[List[Dict[str, Any]]] = None

class CaptchaError(Error, Captcha):
    pass
    # captcha: Captcha
    # captcha_sid: int
    # is_refresh_enabled: bool
    # captcha_img: str
    # captcha_ts: float
    # captcha_attempt: int
    # captcha_ratio: float
    # redirect_uri: str
    # is_sound_captcha_available: bool
    # captcha_track: Optional[str] = None
    # uiux_changes: Optional[bool] = None