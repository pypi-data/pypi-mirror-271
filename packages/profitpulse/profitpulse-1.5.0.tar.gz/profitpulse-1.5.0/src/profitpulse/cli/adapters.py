"""
Adapters bridge the CLI frameworks and the application services by creating the
service inputs and handling the output for printing.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from gogotable import gogotable
from turbofan.database import Database, Session

from profitpulse.data.accounts import Accounts
from profitpulse.data.pulse_view import PulseView
from profitpulse.data.transactions import Transactions
from profitpulse.data.views import AccountsView, TransactionsView
from profitpulse.gateways.cgdfile import GatewayCGDFile  # type: ignore
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money
from profitpulse.services.close_account import (
    CloseAccountRequester,
    CloseAccountService,
)
from profitpulse.services.delete_account import (
    DeleteAccountRequester,
    DeleteAccountService,
)
from profitpulse.services.deposit_into_account import (
    DepositIntoAccountRequester,
    DepositIntoAccountService,
)
from profitpulse.services.import_transactions import (
    ImportTransactionsRequester,
    ImportTransactionsService,
)
from profitpulse.services.open_account import (
    AccountAlreadyExistsError,
    OpenAccountRequester,
    OpenAccountService,
)
from profitpulse.services.revalue import RevalueAccountRequester, RevalueAccountService

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

database_path = Path.home() / Path("Library/Application Support/Profitpulse")


def report(
    seller: Optional[str],
    since: Optional[datetime] = None,
    on: Optional[datetime] = None,
) -> None:
    """
    Shows a report of all transactions in all accounts given the provided
     parameters:
     - seller: The provider or recipient of the value
     - since: The data from which the transactions should be shown
     - on: A specific date for which transactions should be shown
    """

    db = Database(database_path)
    with Session(db.engine) as session:
        view = TransactionsView(session, seller, since, on)

        transactions, total = view.data
        if seller:
            print(f"Description: '{seller}', Value: {round(total, 2)}")
            return

        for t in transactions:
            print(f"Description: '{t['description']:>22}', Value: {t['value']:>10}")


def pulse() -> None:
    """
    Shows the current wealth status.
    """

    headers = ["Account Name", "Status", "Invested", "Current", "Performance"]

    db = Database(database_path)
    with Session(db.engine) as session:
        view = PulseView(session)
        lines = gogotable(headers, view.data)
        for line in lines:
            print(line)


class RevalueAccountRequest(RevalueAccountRequester):
    def __init__(self, account_name: str, value: int) -> None:
        self._account_name = account_name
        self._value = value

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)

    @property
    def value(self) -> Money:
        return Money(self._value)


def revalue(cent_amount: int, account_name: str) -> None:
    """
    Revalues an asset to reflect it's current worth.
    """
    db = Database(database_path)
    with Session(db.engine) as session:
        request = RevalueAccountRequest(account_name, cent_amount)
        accounts = Accounts(session)
        service = RevalueAccountService(accounts)
        service.execute(request)
        session.commit()


def reset() -> None:
    """
    Resets the application by removing the database.
    """
    db = Database(database_path)
    db.remove()


class RequestImportTransactions(ImportTransactionsRequester):
    def __init__(self, account_name: str) -> None:
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def import_file(file_path: Path, account_name: str) -> None:
    """
    Imports a file with all the transactions for a specific asset.
    """
    db = Database(database_path)
    with Session(db.engine) as session:
        gateway_cgd = GatewayCGDFile(file_path)
        transactions = Transactions(session)
        accounts = Accounts(session)
        service = ImportTransactionsService(gateway_cgd, transactions, accounts)
        request = RequestImportTransactions(account_name)
        service.execute(request)
        session.commit()


class DepositRequest(DepositIntoAccountRequester):
    def __init__(
        self, cent_amount: int, account_name: str, comment: Optional[str] = None
    ) -> None:
        self._cent_amount = cent_amount
        self._account_name = account_name
        self._comment = comment

    @property
    def amount(self) -> Money:
        return Money(self._cent_amount)

    @property
    def comment(self) -> Optional[Comment]:
        return Comment(self._comment) if self._comment else None

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def deposit(cent_amount: int, account_name: str, comment: Optional[str] = None) -> None:
    """
    Appreciate an asset by increasing it's value.
    """
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DepositRequest(cent_amount, account_name, comment)
        service = DepositIntoAccountService(accounts)
        service.execute(request)

        session.commit()


def transfer(cent_amount: int, from_account_name: str, to_account_name: str) -> None:
    """
    Transfers value from an asset to another asset.
    """
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DepositRequest(cent_amount, from_account_name)
        service = DepositIntoAccountService(accounts)
        service.execute(request)

        request = DepositRequest(-cent_amount, to_account_name)
        service = DepositIntoAccountService(accounts)
        service.execute(request)

        session.commit()


def show_accounts() -> None:
    """
    Shows all assets and their current value.
    """
    with Session(Database(database_path).engine) as session:
        data = AccountsView(session).data
        if not data:
            return

        headers = ["Name", "Balance", "Status", "Comment"]
        lines = gogotable(headers, data)
        for line in lines:
            print(line)


class OpenAccountRequest(OpenAccountRequester):
    def __init__(self, name: str) -> None:
        self._name = AccountName(name)

    @property
    def account_name(self) -> AccountName:
        return self._name


def open_account(name: str) -> None:
    """
    Creates a new asset.
    """
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = OpenAccountRequest(name)
        try:
            OpenAccountService(accounts).execute(request)
        except AccountAlreadyExistsError as e:
            print(str(e))
            return

        session.commit()


class CloseAccountRequest(CloseAccountRequester):
    def __init__(self, account_name: str) -> None:
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def close_account(name: str) -> None:
    """
    Divests an asset from your wealth but the keeping it's history.
    """
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = CloseAccountRequest(name)
        CloseAccountService(accounts).execute(request)
        session.commit()


class DeleteAccountRequest(DeleteAccountRequester):
    def __init__(self, account_name: str) -> None:
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def delete_account(name: str) -> None:
    """
    Completely deletes an asset.
    """
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DeleteAccountRequest(name)
        DeleteAccountService(accounts).execute(request)
        session.commit()
