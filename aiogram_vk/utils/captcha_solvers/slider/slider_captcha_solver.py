import asyncio
import base64
import json
import re
from dataclasses import dataclass
from typing import Literal, Optional
from urllib.parse import parse_qs, urlencode, urlparse

from curl_cffi import AsyncSession, Response
from pydantic import BaseModel

from aiogram_vk.types.captcha import Captcha, CaptchaAnswer
from aiogram_vk.utils.captcha_solvers.base import CaptchaSolver

from .make_hash import perform_pow
from .solve_image import solve_image


class CaptchaSettings(BaseModel):
    type: Literal["slider", "sound"]
    settings: str


class InitialParams(BaseModel):
    cookies: dict
    captcha_settings: list[CaptchaSettings]
    pow_input: str
    difficulty: int
    show_captcha_type: str


class CaptchaContent(BaseModel):
    extension: Literal["jpeg", "wav"]
    image: str
    status: Literal["OK"] | Literal["ERROR"]
    steps: Optional[list[int]] = None
    track: str


class CaptchaResponse(BaseModel):
    response: CaptchaContent


class SliderCaptchaSolver(CaptchaSolver):
    _headers = {
        "accept": "*/*",
        "accept-language": "ru-RU,ru;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "origin": "https://id.vk.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://id.vk.com/",
        "sec-ch-ua": '"Not?A_Brand";v="99", "Chromium";v="130"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    async def _fetch_init_params(
        self, session: AsyncSession[Response], captcha: Captcha
    ) -> InitialParams:
        parsed_params = parse_qs(urlparse(captcha.redirect_uri).query)
        r = await session.get(
            captcha.redirect_uri,
            headers=self._headers,
            params={k: v[0] for k, v in parsed_params.items()},
        )

        cookies = {
            "remixlang": r.cookies.get("remixlang") or "",
            "remixstlid": r.cookies.get("remixstlid") or "",
            "remixstid": r.cookies.get("remixstid") or "",
        }

        init_params = re.search(r"window\.init\s*=\s*({.*?});", r.text, re.DOTALL)

        captcha_settings = re.search(r"settings\":\"(.+?)\"", r.text)
        pow_input = re.search(r"powInput = \"(.+?)\"", r.text)
        difficulty = re.search(r"const difficulty = (\d+);", r.text)
        captcha_type = re.search(r"show_captcha_type\":\"(.+?)\"", r.text)
        assert init_params
        init_params = json.loads(init_params.group(1))
        if not captcha_settings or not pow_input or not difficulty or not captcha_type:
            raise Exception("Captcha not found")

        captcha_settings = json.loads(f'"{captcha_settings.group(1)}"')
        pow_input = pow_input.group(1)
        difficulty = int(difficulty.group(1))
        captcha_type = captcha_type.group(1)

        return InitialParams(
            cookies=cookies,
            captcha_settings=init_params["data"]["captcha_settings"],
            pow_input=pow_input,
            difficulty=difficulty,
            show_captcha_type=init_params["data"]["show_captcha_type"],
        )

    async def _hook_captcha_settings(
        self, session: AsyncSession[Response], session_token: str, initial_params: InitialParams
    ):
        r = await session.post(
            "https://api.vk.com/method/captchaNotRobot.settings",
            data=f"session_token={session_token}&domain=vk.com&captcha_settings={initial_params.captcha_settings}",
            headers=self._headers,
            params={
                "v": "5.131",
            },
        )

    async def _get_captcha_content(
        self,
        session: AsyncSession[Response],
        session_token: str,
        initial_params: InitialParams,
        captcha_settings: str,
    ):
        r = await session.post(
            "https://api.vk.com/method/captchaNotRobot.getContent",
            data=urlencode(
                {
                    "session_token": session_token,
                    "domain": "vk.com",
                    "captcha_settings": captcha_settings,
                    "access_token": "",
                }
            ),
            headers=self._headers,
            cookies=initial_params.cookies,
            params={
                "v": "5.131",
            },
        )
        data = r.json()
        return CaptchaResponse.model_validate(data).response


    async def _hook_component_done(
        self, session: AsyncSession[Response], session_token: str, initial_params: InitialParams
    ):
        await session.post(
            "https://api.vk.com/method/captchaNotRobot.componentDone?v=5.131",
            data=urlencode(
                {
                    "session_token": session_token,
                    "domain": "vk.com",
                    "access_token": "",
                }
            ),
            headers=self._headers,
            cookies=initial_params.cookies,
            params={
                "v": "5.131",
            },
        )

    async def __call__(self, captcha: Captcha, remixuas: Optional[str] = None) -> CaptchaAnswer:
        session = AsyncSession[Response](
            verify=False,
            impersonate="chrome131",
            cookies={"remixuas": remixuas} if remixuas else {},
        )
        session_token = parse_qs(captcha.redirect_uri)["session_token"][0]
        initial_params = await self._fetch_init_params(session, captcha)

        await self._hook_captcha_settings(session, session_token, initial_params)

        steps = {}
        captchas = {i.type: i for i in initial_params.captcha_settings}
        if (captcha_settings := captchas.get("slider")) is not None:
            captcha_content = await self._get_captcha_content(
                session, session_token, initial_params, captcha_settings.settings
            )
            assert captcha_content.steps
            await self._hook_component_done(session, session_token, initial_params)
            A, steps = solve_image(captcha_content.image, captcha_content.steps)

        h = perform_pow(initial_params.pow_input, initial_params.difficulty)
        data = {
            "accelerometer": "[]",
            "gyroscope": "[]",
            "motion": "[]",
            "cursor": "[]",
            "taps": "[]",
            "session_token": session_token,
            "domain": "vk.com",
            "hash": h,
            "answer": base64.b64encode(
                json.dumps(
                    {
                        "value": steps,
                    }
                ).encode()
            ),
            "access_token": "",
        }
        response = await session.post(
            "https://api.vk.com/method/captchaNotRobot.check",
            params={
                "v": "5.131",
            },
            cookies=initial_params.cookies,
            headers=self._headers,
            data=urlencode(data),
            impersonate="chrome131",
        )
        if response.json()["response"]["status"] != "OK":
            return await self(captcha)
        return CaptchaAnswer(
            captcha_sid=captcha.captcha_sid,
            success_token=response.json()["response"]["success_token"],
        )
