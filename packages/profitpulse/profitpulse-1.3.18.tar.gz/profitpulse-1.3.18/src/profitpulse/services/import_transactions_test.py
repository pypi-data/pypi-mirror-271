# type: ignore
import pytest

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.services.deposit_into_account import AccountDoesNotExistError
from profitpulse.services.import_transactions import ServiceImportTransactions


class AccountsStub:
    def __getitem__(self, account_name: AccountName) -> Account:
        return Account(account_name)


class RequestStub:
    @property
    def account_name(self) -> AccountName:
        return AccountName("TheAccountName")


def test_append_zero_transactions_when_no_transactions_to_append() -> None:
    request = RequestStub()
    accounts = AccountsStub()
    source_transactions = []
    transactions = []
    service = ServiceImportTransactions(
        source_transactions,
        transactions,
        accounts,
    )

    service.execute(request)

    assert len(transactions) == 0  # nosec


class TransactionsStub:
    def __init__(self) -> None:
        self._transactions = []  # type: ignore

    def append(self, transaction, account_name: AccountName):
        self._transactions.append(transaction)

    def __len__(self):
        return len(self._transactions)


def test_append_one_transaction_when_one_transaction_available_in_source():
    request = RequestStub()
    accounts = AccountsStub()
    source_transactions = [{}]
    transactions = TransactionsStub()
    service = ServiceImportTransactions(
        source_transactions,
        transactions,
        accounts,
    )

    service.execute(request)

    assert len(transactions) == 1  # nosec


class AccountNotFounStub:
    def __getitem__(self, _):
        raise KeyError


def test_raise_error_if_account_not_found() -> None:
    request = RequestStub()
    accounts = AccountNotFounStub()
    transactions = []
    source_transactions = [{}]
    service = ServiceImportTransactions(
        source_transactions,
        transactions,
        accounts,
    )
    with pytest.raises(AccountDoesNotExistError, match="Account does not exist"):
        service.execute(request)
