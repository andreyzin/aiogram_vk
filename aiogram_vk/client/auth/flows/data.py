from dataclasses import dataclass, field

from .utils import generate_device_id


@dataclass
class AuthCredentials:
    page_config: dict
    remixuas: str
    sid: str
    can_skip_password: bool
    device_id: str = field(default_factory=generate_device_id)

    @property
    def app_id(self) -> str:
        """ID приложения, через которое выполняется вход."""
        return self.page_config["auth"]["host_app_id"]

    @property
    def uuid(self) -> str:
        """
        Уникальный идентификатор запроса.

        (вероятно, временный для конкретного входа).
        """
        return self.page_config["data"]["uuid"]

    @property
    def access_token(self) -> str:
        """Токен доступа."""
        return self.page_config["auth"]["access_token"]

    @property
    def anonymous_token(self) -> str:
        """Анонимный токен доступа."""
        return self.page_config["auth"]["anonymous_token"]


@dataclass
class ConnectAuthorizeCookies:
    p: str
    remixsid: str
