import abc
import typing
from typing import Optional

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money


class AccountAlreadyExistsError(Exception):
    def __str__(self) -> str:
        return "An account with the same name already exists"


class Accounts(typing.Protocol):
    def get(
        self, account_name: AccountName
    ) -> Optional[Account]: ...  # pragma: no cover

    def __setitem__(
        self, account_name: AccountName, account: Account
    ) -> None: ...  # pragma: no cover


class OpenAccountRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover


class OpenAccountService:
    def __init__(self, accounts: Accounts):
        self.accounts = accounts

    def execute(self, request: OpenAccountRequester) -> None:
        if self.accounts.get(request.account_name):
            raise AccountAlreadyExistsError()

        account = Account(request.account_name)
        account.deposit(Money(0), comment=Comment("Account Opening"))
        self.accounts[request.account_name] = account
