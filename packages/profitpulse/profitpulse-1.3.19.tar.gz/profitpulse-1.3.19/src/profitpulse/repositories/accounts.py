from typing import Optional

import pastperfect
from turbofan.database import text

from profitpulse.lib.account import Account
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money

OPEN = "O"
CLOSED = "C"


class Accounts:
    """
    Accounts implement the AccountsRepository protocol.
    """

    def __init__(self, session):
        self._session = session

    def __len__(self):
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

    def __setitem__(self, account_name: AccountName, account: Account):
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
            INSERT INTO balance (account_id, value, description)
                 VALUES ((SELECT id FROM account WHERE name = :name), :value, :comment)
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(
            name=str(account.name),
            value=str(account.balance.cents),
            comment=str(account.last_comment) if account.last_comment else None,
        )
        self._session.execute(prepared_statement)

        events = pastperfect.Events(self._session)
        events.append(
            pastperfect.Event(
                name="DEPOSIT",
                data={"name": str(account.name), "balance": account.balance.cents},
            )
        )

    def append(self, account: Account):
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
        account_details = [
            account_name,
            "0.00",
            "Open" if row[1] == OPEN else "Closed",
            row[2] if row[2] else "",
        ]
        for event in events:
            if not event.data.get("name") == account_name:
                continue

            account_details[1] = Money(event.data.get("balance"))

        return Account(
            AccountName(row[0]),
            balance=account_details[1],
            closed=True if row[1] == CLOSED else False,
            comment=Comment(row[2] if row[2] else ""),
        )

    def __delitem__(self, account_name: AccountName):
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
