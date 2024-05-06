"""Lego handlers."""

import asyncio
from collections.abc import Callable
from typing import TypeVar

import result
from typing_extensions import assert_never

from lego_handlers.components import AsyncCommand, Command, DomainEvent, Err, Out


async def run_and_collect_events(
    cmd: Command[Out, Err] | AsyncCommand[Out, Err],
) -> result.Result[tuple[Out, list[DomainEvent]], Err]:
    domain_events: list[DomainEvent] = []
    match cmd:
        case Command():
            cmd_result = cmd.run(domain_events=domain_events)
        case AsyncCommand():
            cmd_result = await cmd.run(domain_events=domain_events)
        case _:
            assert_never(cmd)

    match cmd_result:
        case result.Err():
            return cmd_result
        case result.Ok(output_data):
            return result.Ok((output_data, domain_events))
        case _:
            assert_never(cmd_result)


T = TypeVar("T")


async def process_result(
    cmd_result: result.Result[tuple[Out, list[DomainEvent]], Err],
    client_handler: Callable[[result.Result[Out, Err]], T],
    *,
    publish_events: bool,
) -> T:
    output_data_or_err: result.Result[Out, Err]
    match cmd_result:
        case result.Ok():
            output_data, domain_events = cmd_result.unwrap()
            if publish_events:
                await _publish_events(events=domain_events)
            output_data_or_err = result.Ok(output_data)
        case result.Err():
            output_data_or_err = cmd_result
        case _:
            assert_never(cmd_result)

    return client_handler(output_data_or_err)


async def _publish_events(events: list[DomainEvent]) -> None:
    """Publish events."""
    await asyncio.gather(
        *(event.publish() for event in events), return_exceptions=False
    )
