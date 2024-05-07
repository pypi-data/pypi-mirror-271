import abc

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.money import Money
from profitpulse.services.errors import AccountNotFoundError


class RevalueAccountRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover

    @property
    @abc.abstractmethod
    def value(self) -> Money: ...  # pragma: no cover


class RevalueAccountAccountCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover

    @abc.abstractmethod
    def __setitem__(
        self, account_name: AccountName, account: Account
    ) -> None: ...  # pragma: no cover


class RevalueAccountService:
    def __init__(self, accounts: RevalueAccountAccountCollector):
        self.accounts = accounts

    def execute(self, request: RevalueAccountRequester) -> None:
        try:
            account = self.accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(request.account_name)

        account.revalue(request.value)

        self.accounts[request.account_name] = account
