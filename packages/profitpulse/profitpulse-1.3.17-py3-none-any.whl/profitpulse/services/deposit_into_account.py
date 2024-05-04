import abc
import typing
from typing import Optional

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money


class AccountDoesNotExistError(Exception):
    def __str__(self) -> str:
        return "Account does not exist"


class Accounts(typing.Protocol):
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover

    def __setitem__(
        self, account_name: AccountName, account: Account
    ) -> None: ...  # pragma: no cover


class DepositIntoAccountRequest(typing.Protocol):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover

    @property
    @abc.abstractmethod
    def comment(self) -> Optional[Comment]: ...  # pragma: no cover

    @property
    @abc.abstractmethod
    def amount(self) -> Money: ...  # pragma: no cover


class ServiceDepositIntoAccount:
    def __init__(self, accounts: Accounts):
        self._accounts = accounts

    def execute(self, request: DepositIntoAccountRequest) -> None:
        try:
            account = self._accounts[request.account_name]
        except KeyError:
            raise AccountDoesNotExistError()

        account.deposit(request.amount, comment=request.comment)

        self._accounts[request.account_name] = account
