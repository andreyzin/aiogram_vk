from typing import Optional

from pydantic import BaseModel, model_validator


class CaptchaInfo(BaseModel):
    url: str
    sid: str
    track: Optional[str] = None


class Captcha(BaseModel):
    error: str = "Captcha needed"
    captcha_sid: int
    is_refresh_enabled: bool
    captcha_img: str
    captcha_ts: float
    captcha_attempt: int
    captcha_ratio: float
    redirect_uri: str
    is_sound_captcha_available: bool
    captcha_track: Optional[str] = None
    uiux_changes: Optional[bool] = None


class CaptchaAnswer(BaseModel):
    captcha_sid: int
    # One of success_token or key or both
    success_token: Optional[str] = None
    key: Optional[str] = None

    @model_validator(mode="after")
    def check_token_or_key(self):
        if not (self.success_token or self.key):
            raise ValueError("Either 'success_token' or 'key' must be provided (at least one).")
        return self
