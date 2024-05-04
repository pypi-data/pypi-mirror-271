import abc
import typing

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName


class AccountNotFoundError(Exception):
    def __init__(self, account_name: AccountName) -> None:
        self._account_name = account_name

    def __str__(self) -> str:
        return f"Could not find an account with name '{self._account_name}'"


class CloseAccountRequester(typing.Protocol):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover


class Accounts(typing.Protocol):
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover

    def append(self, account: Account) -> None: ...  # pragma: no cover


class CloseAccountService:
    """
    Closes an account.
    """

    def __init__(self, accounts: Accounts) -> None:
        self.accounts = accounts

    def execute(self, request: CloseAccountRequester) -> None:
        try:
            account = self.accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(request.account_name)

        account.close()

        self.accounts.append(account)
