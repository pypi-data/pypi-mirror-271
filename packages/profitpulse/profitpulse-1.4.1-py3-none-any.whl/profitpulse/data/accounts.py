import typing
from enum import Enum
from typing import Optional

import pastperfect
from turbofan.database import text

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money
from profitpulse.services.close_account import CloseAccountAccountCollector
from profitpulse.services.delete_account import DeleteAccountAccountCollector
from profitpulse.services.deposit_into_account import DepositIntoAccountAccountCollector
from profitpulse.services.import_transactions import ImportTransactionsAccountCollector
from profitpulse.services.open_account import OpenAccountAccountCollector
from profitpulse.services.snapshot_account import SnapshotAccountAccountCollector

OPEN = "O"
CLOSED = "C"


# Once python3.9 and python.3.10 support is dropped, we can use
# https://docs.python.org/3/library/enum.html#enum.StrEnum
class StrEnum(str, Enum):
    pass


class PulseEvent(StrEnum):
    MONEY_DEPOSIT = "1"
    TRANSACTION_IMPORTED = "2"
    ACCOUNT_SNAPSHOT = "3"


class Accounts(
    CloseAccountAccountCollector,
    DeleteAccountAccountCollector,
    OpenAccountAccountCollector,
    DepositIntoAccountAccountCollector,
    ImportTransactionsAccountCollector,
    SnapshotAccountAccountCollector,
):
    """
    Accounts implement the AccountsRepository protocol.
    """

    def __init__(self, session: typing.Any) -> None:
        self._session = session

    def __len__(self) -> None:
        sql_stmt = """
            SELECT COUNT(*) FROM account
        """
        prepared_statement = text(sql_stmt)
        row = self._session.execute(prepared_statement).first()
        return row[0]

    def get(self, account_name: AccountName) -> Optional[Account]:
        try:
            return self[account_name]
        except KeyError:
            return None

    def __setitem__(self, account_name: AccountName, account: Account) -> None:

        is_a_new_account = False
        try:
            self[account_name]
        except KeyError:
            is_a_new_account = True

        sql_stmt = """
            INSERT OR REPLACE INTO account (name, status)
                 VALUES (:name, :status)
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(
            name=str(account.name),
            status=CLOSED if account.closed else OPEN,
        )
        self._session.execute(prepared_statement)

        sql_stmt = """
            INSERT INTO balance (account_id, description)
                 VALUES ((SELECT id FROM account WHERE name = :name), :comment)
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(
            name=str(account.name),
            comment=str(account.last_comment) if account.last_comment else None,
        )
        self._session.execute(prepared_statement)

        events = pastperfect.Events(self._session)

        events.append(
            pastperfect.Event(
                name=PulseEvent.ACCOUNT_SNAPSHOT,
                data={"name": str(account.name), "balance": account.balance.cents},
            )
        )

        if is_a_new_account:
            events.append(
                pastperfect.Event(
                    name=PulseEvent.MONEY_DEPOSIT,
                    data={"name": str(account.name), "balance": account.balance.cents},
                )
            )

        for deposit in account.deposit_list():
            events.append(
                pastperfect.Event(
                    name=PulseEvent.MONEY_DEPOSIT,
                    data={"name": str(account.name), "balance": deposit.cents},
                )
            )

    def append(self, account: Account) -> None:
        self[account.name] = account

    def __getitem__(self, account_name: AccountName) -> Account:
        sql_stmt = """
            SELECT account.name as name,
                   account.status,
                   balance.description
              FROM account
         LEFT JOIN balance
                ON account.id = balance.account_id
             WHERE account.name = :name
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=str(account_name))
        row = self._session.execute(prepared_statement).first()
        if not row:
            raise KeyError

        events = pastperfect.Events(self._session)
        account_name = row[0]
        balance = Money(0)
        for event in events:
            if (
                event.name != PulseEvent.ACCOUNT_SNAPSHOT
                or event.data.get("name") != account_name
            ):
                continue

            balance = Money(event.data.get("balance"))

        return Account(
            AccountName(row[0]),
            balance=balance,
            closed=True if row[1] == CLOSED else False,
            comment=Comment(row[2] if row[2] else ""),
        )

    def __delitem__(self, account_name: AccountName) -> None:
        sql_stmt = """
            DELETE FROM balance
                  WHERE account_id = (SELECT id FROM account WHERE name = :name)
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=str(account_name))
        self._session.execute(prepared_statement)

        sql_stmt = """
            DELETE FROM account
                  WHERE name = :name
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=str(account_name))
        self._session.execute(prepared_statement)
