import abc

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.services.errors import AccountNotFoundError


class DeleteAccountRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover


class DeleteAccountAccountCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover

    @abc.abstractmethod
    def __delitem__(self, account_name: AccountName) -> None: ...  # pragma: no cover


class DeleteAccountService:
    def __init__(self, accounts: DeleteAccountAccountCollector) -> None:
        self._accounts = accounts

    def execute(self, request: DeleteAccountRequester) -> None:
        try:
            account = self._accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(account_name=request.account_name)

        account.prepare_deletion()

        del self._accounts[request.account_name]
