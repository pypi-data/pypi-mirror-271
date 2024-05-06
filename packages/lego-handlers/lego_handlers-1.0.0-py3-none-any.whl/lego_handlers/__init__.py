"""Lego handlers."""

import asyncio
from collections.abc import Callable
from typing import TypeVar

from result import Err, Ok, Result

from lego_handlers.components import (
    DomainError,
    DomainEvent,
    ResponseData,
)

R = TypeVar("R", bound=ResponseData)
T = TypeVar("T")


async def process_result(
    result: Result[tuple[R, list[DomainEvent]], DomainError],
    handler: Callable[[Result[R, DomainError]], T],
    *,
    publish_events: bool,
) -> T:
    match result:
        case Ok((response, events)):
            if publish_events:
                await _publish_events(events=events)
            return handler(Ok(response))
        case Err():
            return handler(result)


async def _publish_events(events: list[DomainEvent]) -> None:
    """Publish events."""
    await asyncio.gather(
        *(event.publish() for event in events), return_exceptions=False
    )
