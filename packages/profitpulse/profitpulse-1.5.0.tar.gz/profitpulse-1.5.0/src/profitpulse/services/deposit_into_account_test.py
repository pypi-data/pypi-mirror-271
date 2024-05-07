import pytest

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money
from profitpulse.services.deposit_into_account import (
    AccountNotFoundError,
    DepositIntoAccountAccountCollector,
    DepositIntoAccountRequester,
    DepositIntoAccountService,
)
from profitpulse.turbofan import assert_string_equals


class AccountsNoAccount(DepositIntoAccountAccountCollector):
    def __getitem__(self, account_name: AccountName) -> Account:
        raise KeyError

    def __setitem__(self, account_name: AccountName, account: Account) -> None:
        pass


class DepositInAccountRequest(DepositIntoAccountRequester):
    @property
    def account_name(self) -> AccountName:
        return AccountName("TheAccountName")

    @property
    def comment(self) -> None:
        return None

    @property
    def amount(self) -> Money:
        return Money(100)


def test_raise_error_if_account_does_not_exist() -> None:
    request = DepositInAccountRequest()
    accounts = AccountsNoAccount()

    service = DepositIntoAccountService(accounts)
    with pytest.raises(
        AccountNotFoundError,
        match="Could not find an account with name 'TheAccountName'",
    ):
        service.execute(request)


class AccountsStub(DepositIntoAccountAccountCollector):
    def __init__(self, account: Account) -> None:
        self._account = account
        self.account_added = False

    def __getitem__(self, account_name: AccountName) -> Account:
        return self._account

    def __setitem__(self, account_name: AccountName, account: Account) -> None:
        self.account_added = True
        self._account = account


def test_save_deposit_into_account() -> None:
    request = DepositInAccountRequest()
    account = Account(AccountName("TheAccountName"))
    accounts = AccountsStub(account)

    service = DepositIntoAccountService(accounts)

    service.execute(request)

    assert accounts.account_added  # nosec
    assert account.last_comment is None  # nosec


class DepositInAccountWithCommentRequest(DepositIntoAccountRequester):
    @property
    def account_name(self) -> AccountName:
        return AccountName("TheAccountName")

    @property
    def comment(self) -> Comment:
        return Comment("A comment")

    @property
    def amount(self) -> Money:
        return Money(100)


def test_inject_the_comment_into_the_account_deposit_when_one_is_defined() -> None:
    request = DepositInAccountWithCommentRequest()
    account = Account(AccountName("TheAccountName"))
    accounts = AccountsStub(account)

    service = DepositIntoAccountService(accounts)

    service.execute(request)

    assert accounts.account_added  # nosec
    assert_string_equals("A comment", account.last_comment)
