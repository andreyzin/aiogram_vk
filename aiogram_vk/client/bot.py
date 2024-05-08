from __future__ import annotations

import io
import pathlib
import warnings
from contextlib import asynccontextmanager
from types import TracebackType
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    BinaryIO,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

import aiofiles

from aiogram_vk.__meta__ import __api_version__
from aiogram_vk.methods import account
from aiogram_vk.utils.token import extract_bot_id, validate_token

from ..methods import VkMethod
from ..types import AccountInfo
from .default import DefaultBotProperties
from .session.aiohttp import AiohttpSession
from .session.base import BaseSession

T = TypeVar("T")


class VkBot:
    def __init__(
        self,
        access_token: str,
        session: Optional[BaseSession] = None,
        default: Optional[DefaultBotProperties] = None,
        api_version: str = __api_version__,
    ) -> None:
        """
        VkBot class

        :param access_token: Vk access token
        :param session: HTTP Client session (For example AiohttpSession).
            If not specified it will be automatically created.
        """

        validate_token(access_token)

        if session is None:
            session = AiohttpSession()
        if default is None:
            default = DefaultBotProperties()

        self.session = session

        self.default = default

        self.__token = access_token
        self._api_version = api_version
        self._me: Optional[AccountInfo] = None

    async def __aenter__(self) -> "VkBot":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.session.close()

    @property
    def token(self) -> str:
        return self.__token

    @property
    def api_version(self) -> str:
        return self._api_version

    @property
    def id(self) -> int:
        """
        Get bot ID from token

        :return:
        """
        return extract_bot_id(self.__token)

    @asynccontextmanager
    async def context(self, auto_close: bool = True) -> AsyncIterator[VkBot]:
        """
        Generate bot context

        :param auto_close: close session on exit
        :return:
        """
        try:
            yield self
        finally:
            if auto_close:
                await self.session.close()

    async def me(self) -> AccountInfo:
        """
        Cached alias for getMe method

        :return:
        """
        if self._me is None:  # pragma: no cover
            self._me = await self(account.GetInfo())
        return self._me

    @classmethod
    async def __download_file_binary_io(
        cls, destination: BinaryIO, seek: bool, stream: AsyncGenerator[bytes, None]
    ) -> BinaryIO:
        async for chunk in stream:
            destination.write(chunk)
            destination.flush()
        if seek is True:
            destination.seek(0)
        return destination

    @classmethod
    async def __download_file(
        cls, destination: Union[str, pathlib.Path], stream: AsyncGenerator[bytes, None]
    ) -> None:
        async with aiofiles.open(destination, "wb") as f:
            async for chunk in stream:
                await f.write(chunk)

    @classmethod
    async def __aiofiles_reader(
        cls, file: str, chunk_size: int = 65536
    ) -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(file, "rb") as f:
            while chunk := await f.read(chunk_size):
                yield chunk

    async def download_file(
        self,
        file_path: str,
        destination: Optional[Union[BinaryIO, pathlib.Path, str]] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        seek: bool = True,
    ) -> Optional[BinaryIO]:
        """
        Download file by file_path to destination.

        If you want to automatically create destination (:class:`io.BytesIO`) use default
        value of destination and handle result of this method.

        :param file_path: File path on Telegram server (You can get it from :obj:`aiogram.types.File`)
        :param destination: Filename, file path or instance of :class:`io.IOBase`. For e.g. :class:`io.BytesIO`, defaults to None
        :param timeout: Total timeout in seconds, defaults to 30
        :param chunk_size: File chunks size, defaults to 64 kb
        :param seek: Go to start of file when downloading is finished. Used only for destination with :class:`typing.BinaryIO` type, defaults to True
        """
        if destination is None:
            destination = io.BytesIO()

        close_stream = False
        if self.session.api.is_local:
            stream = self.__aiofiles_reader(
                str(self.session.api.wrap_local_file.to_local(file_path)), chunk_size=chunk_size
            )
            close_stream = True
        else:
            url = self.session.api.file_url(self.__token, file_path)
            stream = self.session.stream_content(
                url=url,
                timeout=timeout,
                chunk_size=chunk_size,
                raise_for_status=True,
            )

        try:
            if isinstance(destination, (str, pathlib.Path)):
                await self.__download_file(destination=destination, stream=stream)
                return None
            return await self.__download_file_binary_io(
                destination=destination, seek=seek, stream=stream
            )
        finally:
            if close_stream:
                await stream.aclose()

    async def __call__(self, method: VkMethod[T], request_timeout: Optional[int] = None) -> T:
        """
        Call API method

        :param method:
        :return:
        """
        return await self.session(self, method, timeout=request_timeout)

    def __hash__(self) -> int:
        """
        Get hash for the token

        :return:
        """
        return hash(self.__token)

    def __eq__(self, other: Any) -> bool:
        """
        Compare current bot with another bot instance

        :param other:
        :return:
        """
        if not isinstance(other, VkBot):
            return False
        return hash(self) == hash(other)
