from abc import ABC, abstractmethod

from aiogram_vk.types.captcha import Captcha, CaptchaAnswer


class CaptchaSolver(ABC):
    @abstractmethod
    async def __call__(self, captcha: Captcha) -> CaptchaAnswer:
        raise NotImplementedError
