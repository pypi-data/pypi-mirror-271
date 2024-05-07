import abc

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.transaction import Transaction
from profitpulse.services.deposit_into_account import AccountNotFoundError


class ImportTransactionsTransactionGater(abc.ABC):
    def __iter__(self) -> None:
        pass  # pragma: no cover


class ImportTransactionsTransactionCollector(abc.ABC):
    @abc.abstractmethod
    def append(self, transaction: Transaction, account_name: AccountName) -> None:
        pass  # pragma: no cover


class ImportTransactionsRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def account_name(self) -> AccountName: ...  # pragma: no cover


class ImportTransactionsAccountCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, account_name: AccountName) -> Account: ...  # pragma: no cover


class ImportTransactionsService:
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: ImportTransactionsTransactionGater,
        transactions: ImportTransactionsTransactionCollector,
        accounts: ImportTransactionsAccountCollector,
    ) -> None:
        self.transactions = transactions_gateway
        self._transactions = transactions
        self._accounts = accounts

    def execute(self, request: ImportTransactionsRequester) -> None:
        try:
            _ = self._accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(request.account_name)

        for transaction in self.transactions:  # type: ignore
            self._transactions.append(transaction, request.account_name)
