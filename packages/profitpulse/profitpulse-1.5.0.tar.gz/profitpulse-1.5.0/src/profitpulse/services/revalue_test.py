import pytest

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.money import Money
from profitpulse.services.revalue import (
    AccountNotFoundError,
    RevalueAccountAccountCollector,
    RevalueAccountRequester,
    RevalueAccountService,
)


class RevalueAccountRequest(RevalueAccountRequester):
    def __init__(self, account_name: str, value: int):
        self._account_name = AccountName(account_name)
        self._value = value

    @property
    def value(self) -> Money:
        return Money(self._value)

    @property
    def account_name(self) -> AccountName:
        return self._account_name


class Accounts(RevalueAccountAccountCollector):
    def __init__(self, account: Account) -> None:
        self.account = account

    def __getitem__(self, account_name: AccountName) -> Account:
        return self.account

    def __setitem__(self, account_name: AccountName, account: Account) -> None:
        self.account = account


def test_return_error_when_account_does_not_exist() -> None:
    account_name = "TheAccountName"
    request = RevalueAccountRequest(account_name, 0)

    service = RevalueAccountService(dict())  # type: ignore

    with pytest.raises(
        AccountNotFoundError,
        match=f"Could not find an account with name '{account_name}'",
    ):
        service.execute(request)


def test_revalue_account() -> None:
    account_name = "TheAccountName"
    accounts = Accounts(Account(account_name=AccountName(account_name)))

    request = RevalueAccountRequest(account_name, 1)
    service = RevalueAccountService(accounts)

    service.execute(request)

    assert accounts.account.balance == Money(1)  # nosec
