import abc

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.services.errors import AccountNotFoundError


class CloseAccountRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover


class CloseAccountAccountCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover

    @abc.abstractmethod
    def append(self, account: Account) -> None: ...  # pragma: no cover


class CloseAccountService:
    """
    Closes an account.
    """

    def __init__(self, accounts: CloseAccountAccountCollector) -> None:
        self.accounts = accounts

    def execute(self, request: CloseAccountRequester) -> None:
        try:
            account = self.accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(request.account_name)

        account.close()

        self.accounts.append(account)
