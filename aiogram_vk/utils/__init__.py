from typing import Optional, Protocol

from aiogram_vk.types.captcha import Captcha, CaptchaAnswer
from aiogram_vk.utils.captcha_solvers.base import CaptchaSolver

from .captcha_solvers.slider.slider_captcha_solver import SliderCaptchaSolver


class CaptchaSolverProtocol(Protocol):
    async def __call__(
        self, captcha: Captcha, remixuas: Optional[str] = None
    ) -> CaptchaAnswer: ...


__all__ = [
    "CaptchaSolver",
    "CaptchaSolverProtocol",
    "SliderCaptchaSolver",
]
