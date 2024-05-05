# type: ignore
import abc
import typing

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.transaction import Transaction
from profitpulse.services.deposit_into_account import AccountDoesNotExistError


class GatewayTransactions(typing.Protocol):
    """
    Gateway to transactions.
    """

    def __iter__(self) -> None:
        pass  # pragma: no cover


class RepositoryTransactions(typing.Protocol):
    """
    Repository to transactions.
    """

    def append(self, transaction: Transaction, account_name: AccountName) -> None:
        pass  # pragma: no cover


class ImportTransactionsRequest(abc.ABC):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover


class Accounts(typing.Protocol):
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover


class ServiceImportTransactions:
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: GatewayTransactions,
        transactions: RepositoryTransactions,
        accounts: Accounts,
    ) -> None:
        self.transactions = transactions_gateway
        self._transactions = transactions
        self._accounts = accounts

    def execute(self, request: ImportTransactionsRequest) -> None:
        try:
            _ = self._accounts[request.account_name]
        except KeyError:
            raise AccountDoesNotExistError

        for transaction in self.transactions:
            self._transactions.append(transaction, request.account_name)
