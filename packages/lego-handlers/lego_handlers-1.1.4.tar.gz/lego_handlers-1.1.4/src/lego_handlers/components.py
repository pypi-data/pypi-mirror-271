"""Lego handlers components."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

import result


class DomainError(Exception):
    """Raised when business rule has been violated."""


@dataclass(frozen=True)
class OutputData:
    """Handler response data."""


@dataclass(frozen=True)
class DomainEvent(ABC):
    """Domain Event."""

    @abstractmethod
    async def publish(self) -> None:
        """Publish event."""


Out = TypeVar("Out", bound=OutputData)
Err = TypeVar("Err", bound=DomainError)


@dataclass(frozen=True)
class Command(ABC, Generic[Out, Err]):
    @abstractmethod
    def run(self, domain_events: list[DomainEvent]) -> result.Result[Out, Err]:
        """Execute command."""


@dataclass(frozen=True)
class AsyncCommand(ABC, Generic[Out, Err]):
    @abstractmethod
    async def run(self, domain_events: list[DomainEvent]) -> result.Result[Out, Err]:
        """Execute async command."""
