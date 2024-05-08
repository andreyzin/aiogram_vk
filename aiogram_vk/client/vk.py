from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union

from aiohttp.http import SERVER_SOFTWARE

from aiogram_vk.__meta__ import __version__


class FilesPathWrapper(ABC):
    @abstractmethod
    def to_local(self, path: Union[Path, str]) -> Union[Path, str]:
        pass

    @abstractmethod
    def to_server(self, path: Union[Path, str]) -> Union[Path, str]:
        pass


class BareFilesPathWrapper(FilesPathWrapper):
    def to_local(self, path: Union[Path, str]) -> Union[Path, str]:
        return path

    def to_server(self, path: Union[Path, str]) -> Union[Path, str]:
        return path


class SimpleFilesPathWrapper(FilesPathWrapper):
    def __init__(self, server_path: Path, local_path: Path) -> None:
        self.server_path = server_path
        self.local_path = local_path

    @classmethod
    def _resolve(
        cls, base1: Union[Path, str], base2: Union[Path, str], value: Union[Path, str]
    ) -> Path:
        relative = Path(value).relative_to(base1)
        return base2 / relative

    def to_local(self, path: Union[Path, str]) -> Union[Path, str]:
        return self._resolve(base1=self.server_path, base2=self.local_path, value=path)

    def to_server(self, path: Union[Path, str]) -> Union[Path, str]:
        return self._resolve(base1=self.local_path, base2=self.server_path, value=path)


@dataclass(frozen=True)
class VkAPIClient:
    """
    Base config for API Endpoints
    """

    base: str
    """Base URL"""
    file: str
    client_id: int
    client_secret: str
    user_agent: str = f"{SERVER_SOFTWARE} aiogram_vk/{__version__}"
    """Files URL"""
    is_local: bool = False
    """Mark this server is
    in `local mode <https://core.telegram.org/bots/api#using-a-local-bot-api-server>`_."""
    wrap_local_file: FilesPathWrapper = BareFilesPathWrapper()
    """Callback to wrap files path in local mode"""

    def api_url(self, token: str, method: str) -> str:
        """
        Generate URL for API methods

        :param token: Bot token
        :param method: API method name (case insensitive)
        :return: URL
        """
        return self.base.format(token=token, method=method)

    def file_url(self, token: str, path: str) -> str:
        """
        Generate URL for downloading files

        :param token: Bot token
        :param path: file path
        :return: URL
        """
        return self.file.format(token=token, path=path)

    @classmethod
    def from_base(cls, base: str, **kwargs: Any) -> "VkAPIClient":
        """
        Use this method to auto-generate TelegramAPIServer instance from base URL

        :param base: Base URL
        :return: instance of :class:`TelegramAPIServer`
        """
        base = base.rstrip("/")
        return cls(
            base=f"{base}/bot{{token}}/{{method}}",
            file=f"{base}/file/bot{{token}}/{{path}}",
            **kwargs,
        )


KATE = VkAPIClient(
    base="https://api.vk.com/method/{method}",
    file="https://api.telegram.org/file/bot{token}/{path}",
    user_agent="KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)",
    client_id=2685278,
    client_secret="lxhD8OD7dMsqtXIm5IUY",
)
