from typing import Optional

import pytest

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.services.close_account import (
    AccountNotFoundError,
    CloseAccountAccountCollector,
    CloseAccountRequester,
    CloseAccountService,
)


class CloseAccountRequest(CloseAccountRequester):
    def __init__(self, account_name: str):
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def test_raise_exception_when_account_is_not_found() -> None:
    account_name = "TheAccountName"
    request = CloseAccountRequest(account_name)
    accounts = CloseAccountAccountsRepo()
    service = CloseAccountService(accounts)

    with pytest.raises(
        AccountNotFoundError,
        match="Could not find an account with name 'TheAccountName'",
    ):
        service.execute(request)


class CloseAccountAccountsRepo(CloseAccountAccountCollector):
    def __init__(self, account: Optional[Account] = None) -> None:
        self._account = account

    def __getitem__(self, account_name: AccountName) -> Account:
        if not self._account:
            raise KeyError
        return self._account

    def append(self, account: Account) -> None:
        self._account = account


def test_close_account_when_the_account_exists() -> None:
    account_name = "TheAccountName"
    account = Account(AccountName(account_name))
    accounts = CloseAccountAccountsRepo(account)
    request = CloseAccountRequest(account_name)
    service = CloseAccountService(accounts)

    service.execute(request)

    assert account.closed  # nosec
