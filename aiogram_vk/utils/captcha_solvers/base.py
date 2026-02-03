from abc import ABC, abstractmethod
from typing import Optional

from aiogram_vk.types.captcha import Captcha, CaptchaAnswer


class CaptchaSolver(ABC):
    @abstractmethod
    async def __call__(self, captcha: Captcha, remixuas: Optional[str] = None) -> CaptchaAnswer:
        raise NotImplementedError
