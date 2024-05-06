from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID, uuid4

import lego_handlers
from lego_handlers.components import Command, DomainError, DomainEvent, OutputData
from result import Err, Ok, Result


@dataclass(frozen=True)
class ResponseCreateAccount(OutputData):
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


_DomainErrors: TypeAlias = ZeroInitialBalanceError | NegativeInitialBalanceError


@dataclass(frozen=True)
class CreateAccount(Command[ResponseCreateAccount, _DomainErrors]):
    initial_balance: int

    def run(
        self, domain_events: list[DomainEvent]
    ) -> Result[ResponseCreateAccount, _DomainErrors]:
        if self.initial_balance < 0:
            return Err(NegativeInitialBalanceError())

        if self.initial_balance == 0:
            return Err(ZeroInitialBalanceError())
        domain_events.append(AccountCreated())
        return Ok(
            ResponseCreateAccount(
                account_id=uuid4(), initial_balance=self.initial_balance
            )
        )


def _client_handler(
    result: Result[ResponseCreateAccount, _DomainErrors],
) -> str:
    match result:
        case Ok():
            return "Data"
        case Err():
            return str(result.err())


async def test_run_command() -> None:
    intial_balance = 10
    command_result_and_events = await lego_handlers.run_and_collect_events(
        cmd=CreateAccount(
            initial_balance=intial_balance,
        ),
    )
    assert isinstance(command_result_and_events, Ok)
    response_data, events = command_result_and_events.unwrap()
    assert response_data.initial_balance == intial_balance
    assert len(events) == 1
    assert (
        await lego_handlers.process_result(
            cmd_result=command_result_and_events,
            publish_events=False,
            client_handler=_client_handler,
        )
    ) == "Data"


async def test_error() -> None:
    cmd_result_and_events = await lego_handlers.run_and_collect_events(
        cmd=CreateAccount(
            initial_balance=-10,
        ),
    )

    assert isinstance(cmd_result_and_events, Err)
    assert isinstance(cmd_result_and_events.err(), NegativeInitialBalanceError)
    assert (
        await lego_handlers.process_result(
            cmd_result=cmd_result_and_events,
            publish_events=False,
            client_handler=_client_handler,
        )
    ) == str(NegativeInitialBalanceError())
