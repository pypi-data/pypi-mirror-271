import abc

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName


class AccountNotFoundError(Exception):
    def __init__(self, account_name: AccountName) -> None:
        self._account_name = account_name

    def __str__(self) -> str:
        return f"Could not find an account with name '{self._account_name}'"


class DeleteAccountRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover


class AccountsRepository(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover

    @abc.abstractmethod
    def __delitem__(self, account_name: AccountName) -> None: ...  # pragma: no cover


class ServiceDeleteAccount:
    def __init__(self, accounts: AccountsRepository) -> None:
        self._accounts = accounts

    def execute(self, request: DeleteAccountRequester) -> None:
        try:
            account = self._accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(account_name=request.account_name)

        account.prepare_deletion()

        del self._accounts[request.account_name]
