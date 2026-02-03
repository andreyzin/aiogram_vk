from typing import Optional, Protocol

from pydantic import BaseModel


class AuthEvent(BaseModel):
    name: str
    description: Optional[str] = None


class AuthEventPipeProtocol(Protocol):
    async def __call__(self, event: AuthEvent) -> None:
        pass
