"""
Cli adapters bridge the CLI frameworks with the services use cases and print
data into the screen.
"""

import logging
from pathlib import Path
from typing import Optional

from gogotable import gogotable
from turbofan.database import Database, Session

from profitpulse.cli import console
from profitpulse.gateways.cgdfile import GatewayCGDFile
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money
from profitpulse.repositories.accounts import Accounts
from profitpulse.repositories.transactions import Transactions
from profitpulse.services.close_account import CloseAccountService
from profitpulse.services.delete_account import ServiceDeleteAccount
from profitpulse.services.deposit_into_account import ServiceDepositIntoAccount
from profitpulse.services.import_transactions import ServiceImportTransactions
from profitpulse.services.open_account import (
    AccountAlreadyExistsError,
    OpenAccountService,
)
from profitpulse.views.accounts import AccountsView
from profitpulse.views.transactions import ViewTransactions
from profitpulse.views.views import PulseView

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

database_path = Path.home() / Path("Library/Application Support/Profitpulse")


def report(seller, since, on):
    db = Database(database_path)
    with Session(db.engine) as session:
        view = ViewTransactions(session, seller, since, on)

        transactions, total = view.data
        if not seller:
            if not transactions:
                print("Could not find any transactions!")
                return

            for t in transactions:
                print(f"Description: '{t['description']:>22}', Value: {t['value']:>10}")
            return

        print(f"Description: '{seller}', Value: {round(total, 2)}")


def pulse():
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


def reset():
    db = Database(database_path)
    db.remove()


class RequestImportTransactions:
    def __init__(self, account_name: str) -> None:
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def import_file(file_path: Path, account_name):
    db = Database(database_path)
    with Session(db.engine) as session:
        gateway_cgd = GatewayCGDFile(file_path)
        transactions = Transactions(session)
        accounts = Accounts(session)
        service = ServiceImportTransactions(gateway_cgd, transactions, accounts)
        request = RequestImportTransactions(account_name)
        service.execute(request)
        session.commit()


class DepositRequest:
    def __init__(self, cent_amount, account_name, comment: Optional[str] = None):
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
        return self._account_name


def deposit(cent_amount: int, account_name: str, comment: Optional[str] = None) -> None:
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DepositRequest(cent_amount, account_name, comment)
        service = ServiceDepositIntoAccount(accounts)
        service.execute(request)

        session.commit()


def transfer(cent_amount: int, from_account_name: str, to_account_name: str) -> None:
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DepositRequest(cent_amount, from_account_name)
        service = ServiceDepositIntoAccount(accounts)
        service.execute(request)

        request = DepositRequest(-cent_amount, to_account_name)
        service = ServiceDepositIntoAccount(accounts)
        service.execute(request)

        session.commit()


def show_accounts():
    with Session(Database(database_path).engine) as session:
        data = AccountsView(session).data
        if not data:
            return

        headers = ["Name", "Balance", "Status", "Comment"]
        lines = gogotable(headers, data)
        for line in lines:
            print(line)


class OpenAccountRequest:
    def __init__(self, name):
        self._name = AccountName(name)

    @property
    def account_name(self):
        return self._name


def open_account(name):
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = OpenAccountRequest(name)
        try:
            OpenAccountService(accounts).execute(request)
        except AccountAlreadyExistsError as e:
            msg = console.message(
                str(e) + " " + ", why don't you try again using a different name ?"
            )
            print(msg)

        session.commit()


class CloseAccountRequest:
    def __init__(self, account_name):
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def close_account(name):
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = CloseAccountRequest(name)
        CloseAccountService(accounts).execute(request)
        session.commit()


class DeleteAccountRequest:
    def __init__(self, account_name):
        self._account_name = account_name

    @property
    def account_name(self) -> AccountName:
        return AccountName(self._account_name)


def delete_account(name):
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = DeleteAccountRequest(name)
        ServiceDeleteAccount(accounts).execute(request)
        session.commit()
