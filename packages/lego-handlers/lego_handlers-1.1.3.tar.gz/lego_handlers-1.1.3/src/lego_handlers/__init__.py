"""Lego handlers."""

import asyncio
from collections.abc import Callable
from typing import TypeVar

from result import Err, Ok, Result
from typing_extensions import assert_never

from lego_handlers.components import (
    DomainError,
    DomainEvent,
    ResponseData,
)

T = TypeVar("T")
E = TypeVar("E", bound=DomainError)
R = TypeVar("R", bound=ResponseData)


async def process_result(
    result: Result[tuple[R, list[DomainEvent]], E],
    handler: Callable[[Result[R, E]], T],
    *,
    publish_events: bool,
) -> T:
    match result:
        case Ok(data_and_events):
            response_data, events = data_and_events
            if publish_events:
                await _publish_events(events=events)
            return handler(Ok(response_data))
        case Err(error):
            return handler(Err(error))
        case _:
            assert_never(result)


async def _publish_events(events: list[DomainEvent]) -> None:
    """Publish events."""
    await asyncio.gather(
        *(event.publish() for event in events), return_exceptions=False
    )
