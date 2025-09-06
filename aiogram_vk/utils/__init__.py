from typing import Awaitable, Callable

from aiogram_vk.types.captcha import Captcha, CaptchaAnswer
from aiogram_vk.utils.captcha_solvers.base import CaptchaSolver

from .captcha_solvers.slider.slider_captcha_solver import SliderCaptchaSolver

CaptchaSolverType = Callable[[Captcha], Awaitable[CaptchaAnswer]] | CaptchaSolver

__all__ = [
    "CaptchaSolver",
    "CaptchaSolverType",
    "SliderCaptchaSolver",
]
