from typing import Any, Optional

from aiogram_vk.methods import VkMethod
from aiogram_vk.methods.base import VkType


class AiogramError(Exception):
    """
    Base exception for all aiogram errors.
    """


class DetailedAiogramError(AiogramError):
    """
    Base exception for all aiogram errors with detailed message.
    """

    url: Optional[str] = None

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        message = self.message
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class CallbackAnswerException(AiogramError):
    """
    Exception for callback answer.
    """


class SceneException(AiogramError):
    """
    Exception for scenes.
    """


class UnsupportedKeywordArgument(DetailedAiogramError):
    """
    Exception raised when a keyword argument is passed as filter.
    """


class VkAPIError(DetailedAiogramError):
    """
    Base exception for all Vk API errors.
    """

    label: str = "Vk server says"

    def __init__(
        self,
        method: VkMethod[VkType],
        message: str,
    ) -> None:
        super().__init__(message=message)
        self.method = method

    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"


class VkNetworkError(VkAPIError):
    """
    Base exception for all Vk network errors.
    """

    label = "HTTP Client says"


class VkRetryAfter(VkAPIError):
    """
    Exception raised when flood control exceeds.
    """

    url = "https://core.Vk.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this"

    def __init__(
        self,
        method: VkMethod[VkType],
        message: str,
        retry_after: int,
    ) -> None:
        description = f"Flood control exceeded on method {type(method).__name__!r}"
        if chat_id := getattr(method, "chat_id", None):
            description += f" in chat {chat_id}"
        description += f". Retry in {retry_after} seconds."
        description += f"\nOriginal description: {message}"

        super().__init__(method=method, message=description)
        self.retry_after = retry_after


class ClientDecodeError(AiogramError):
    """
    Exception raised when client can't decode response. (Malformed response, etc.)
    """

    def __init__(self, message: str, original: Exception, data: Any) -> None:
        self.message = message
        self.original = original
        self.data = data

    def __str__(self) -> str:
        original_type = type(self.original)
        return (
            f"{self.message}\n"
            f"Caused from error: "
            f"{original_type.__module__}.{original_type.__name__}: {self.original}\n"
            f"Content: {self.data}"
        )
