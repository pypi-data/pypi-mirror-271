from typing import Dict, Optional

import pytest

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.services.open_account import (
    AccountAlreadyExistsError,
    OpenAccountRequester,
    OpenAccountService,
)


class AccountsStub:
    def __init__(self) -> None:
        self._accounts: Dict[AccountName, Account] = dict()

    def get(self, account_name: AccountName) -> Optional[Account]:
        try:
            return self._accounts[account_name]
        except KeyError:
            return None

    def __setitem__(self, account_name: AccountName, account: Account) -> None:
        self._accounts[account_name] = account


class OpenAccountRequest(OpenAccountRequester):
    def __init__(self, account_name: str):
        self._account_name = AccountName(account_name)

    @property
    def account_name(self) -> AccountName:
        return self._account_name


def test_raise_error_if_an_account_with_same_name_already_exists() -> None:
    account_name = "TheAccountName"
    request = OpenAccountRequest(account_name)
    accounts = AccountsStub()
    service = OpenAccountService(accounts)

    service.execute(request)

    with pytest.raises(
        AccountAlreadyExistsError,
        match="An account with the same name already exists",
    ):
        service.execute(request)


def test_save_account_when_its_a_new_account() -> None:
    request = OpenAccountRequest(account_name="TheAccountName")
    accounts = AccountsStub()
    service = OpenAccountService(accounts)

    service.execute(request)

    assert accounts.get(request.account_name) is not None  # nosec
