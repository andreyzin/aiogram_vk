from typing import Optional

from pydantic import BaseModel


class CaptchaInfo(BaseModel):
    url: str
    sid: str
    track: Optional[str] = None
