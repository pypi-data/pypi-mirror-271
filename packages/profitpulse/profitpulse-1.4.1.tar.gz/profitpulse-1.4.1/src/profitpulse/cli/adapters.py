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
from profitpulse.data.transactions import Transactions
from profitpulse.data.views import AccountsView, PulseView, TransactionsView
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
from profitpulse.services.snapshot_account import (
    SnapshotAccountRequester,
    SnapshotAccountService,
)

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

database_path = Path.home() / Path("Library/Application Support/Profitpulse")


def report(
    seller: Optional[str],
    since: Optional[datetime] = None,
    on: Optional[datetime] = None,
) -> None:
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
    Read all the events and print the current proofit pulse.
    """

    headers = ["Account Name", "Invested", "Current", "Performance"]

    db = Database(database_path)
    with Session(db.engine) as session:
        view = PulseView(session)
        lines = gogotable(headers, view.data)
        for line in lines:
            print(line)


class SnapshotAccountRequest(SnapshotAccountRequester):
    def __init__(self, account_name: str, value: int) -> None:
        self._account_name = account_name
        self._value = value

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)

    @property
    def value(self) -> Money:
        return Money(self._value)


def snapshot(cent_amount: int, account_name: str) -> None:
    db = Database(database_path)
    with Session(db.engine) as session:
        request = SnapshotAccountRequest(account_name, cent_amount)
        accounts = Accounts(session)
        service = SnapshotAccountService(accounts)
        service.execute(request)
        session.commit()


def reset() -> None:
    db = Database(database_path)
    db.remove()


class RequestImportTransactions(ImportTransactionsRequester):
    def __init__(self, account_name: str) -> None:
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def import_file(file_path: Path, account_name: str) -> None:
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
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DepositRequest(cent_amount, account_name, comment)
        service = DepositIntoAccountService(accounts)
        service.execute(request)

        session.commit()


def transfer(cent_amount: int, from_account_name: str, to_account_name: str) -> None:
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
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DeleteAccountRequest(name)
        DeleteAccountService(accounts).execute(request)
        session.commit()
