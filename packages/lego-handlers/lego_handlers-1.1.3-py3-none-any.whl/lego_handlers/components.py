"""Lego handlers components."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class DomainError(Exception):
    """Raised when business rule has been violated."""


@dataclass(frozen=True)
class ResponseData:
    """Handler response data."""


@dataclass(frozen=True)
class DomainEvent(ABC):
    """Domain Event."""

    @abstractmethod
    async def publish(self) -> None:
        """Publish event."""
