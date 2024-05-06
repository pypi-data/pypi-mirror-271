from dataclasses import dataclass
from uuid import UUID, uuid4

import lego_handlers
from lego_handlers.components import (
    DomainError,
    DomainEvent,
    ResponseData,
)
from result import Err, Ok, Result


@dataclass(frozen=True)
class ResponseCreateAccount(ResponseData):
    account_id: UUID
    initial_balance: int


@dataclass(frozen=True)
class AccountCreated(DomainEvent):
    async def publish(self) -> None: ...


class NegativeInitialBalanceError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "Not possible to create account with negative initial balance."
        )


class ZeroInitialBalanceError(DomainError):
    def __init__(self) -> None:
        super().__init__("Not possible to create account with zero initial balance.")


def create_account(
    initial_balance: int,
) -> Result[
    tuple[ResponseCreateAccount, list[DomainEvent]],
    ZeroInitialBalanceError | NegativeInitialBalanceError,
]:
    events: list[DomainEvent] = []
    if initial_balance < 0:
        return Err(NegativeInitialBalanceError())

    if initial_balance == 0:
        return Err(ZeroInitialBalanceError())

    events.append(AccountCreated())

    return Ok(
        (
            ResponseCreateAccount(account_id=uuid4(), initial_balance=initial_balance),
            events,
        )
    )


def _result_hanlder(result: Result[ResponseData, DomainError]) -> str:
    match result:
        case Ok():
            return "Data"
        case Err():
            return str(result)


async def test_run_command() -> None:
    intial_balance = 10
    command_result = create_account(
        initial_balance=intial_balance,
    )
    assert isinstance(command_result, Ok)
    response_data, events = command_result.unwrap()
    assert response_data.initial_balance == intial_balance
    assert len(events) == 1
    await lego_handlers.process_result(
        result=command_result,
        handler=_result_hanlder,
        publish_events=False,
    )


def test_error() -> None:
    command_result = create_account(initial_balance=-10)
    assert isinstance(command_result, Err)
