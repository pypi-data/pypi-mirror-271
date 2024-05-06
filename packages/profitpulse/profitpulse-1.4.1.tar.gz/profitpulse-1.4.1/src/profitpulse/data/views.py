import abc
import typing
from datetime import datetime
from typing import Any

import pastperfect
from turbofan.database import text

from profitpulse.data import accounts as accounts_repository
from profitpulse.data.accounts import PulseEvent
from profitpulse.lib.money import Money


class View(abc.ABC):
    @property
    @abc.abstractmethod
    def data(self) -> Any: ...


class AccountsView(View):
    def __init__(self, session: typing.Any) -> None:
        self._session = session

    @property
    def data(self) -> Any:
        sql_stmt = """
          SELECT account.name as name,
                 account.status,
                 balance.description
            FROM account
       LEFT JOIN balance
              ON account.id = balance.account_id
        """
        rows = self._session.execute(text(sql_stmt))
        accounts = list(rows)
        events = pastperfect.Events(self._session)

        results = []
        for account in accounts:
            account_name = account[0]
            account_details = [
                account_name,
                "0.00",
                "Open" if account[1] == accounts_repository.OPEN else "Closed",
                account[2] if account[2] else "",
            ]
            total_balance = Money(0)
            for event in events:
                if (
                    event.name != PulseEvent.ACCOUNT_SNAPSHOT
                    or event.data.get("name") != account_name
                ):
                    continue

                total_balance = Money(event.data.get("balance"))

            account_details[1] = str(total_balance)

            results.append(account_details)

        return results


class PulseView(View):
    def __init__(self, session: typing.Any):
        self._session = session

    @property
    def data(self) -> typing.Any:
        sql_stmt = """SELECT account.name as name FROM account ORDER BY id ASC"""
        accounts = self._session.execute(text(sql_stmt))

        events = pastperfect.Events(self._session)

        results = []
        for account in accounts:
            account_name = account[0]
            account_details = [""] * 4
            invested = Money(0)
            current = Money(0)

            for event in events:
                if (
                    event.name == PulseEvent.ACCOUNT_SNAPSHOT
                    and event.data.get("name") == account_name
                ):
                    current = Money(event.data.get("balance"))
                    continue

                if (
                    event.name == PulseEvent.MONEY_DEPOSIT
                    and event.data.get("name") == account_name
                ):
                    invested = invested + Money(event.data.get("balance"))

            account_details[0] = account_name
            account_details[1] = str(invested)
            account_details[2] = str(current)
            account_details[3] = str(current - invested)

            results.append(account_details)

        return results


class TransactionsView(View):
    def __init__(
        self,
        session: typing.Any,
        seller: typing.Optional[str] = None,
        since: typing.Optional[datetime] = None,
        on: typing.Optional[datetime] = None,
    ) -> None:
        self._seller = seller.lower() if seller else None
        self._session = session
        self._since = since
        self._on = on

    @property
    def data(self) -> typing.Any:  # noqa
        """
        The data resulting from the view execution.
        """

        if not self._seller:
            events = pastperfect.Events(self._session)
            total_money = Money(0)
            transactions = []
            for event in events:
                if event.name != PulseEvent.TRANSACTION_IMPORTED:
                    continue

                date_of_transaction = datetime.strptime(event.data["date"], "%Y-%m-%d")
                if self._since:
                    if date_of_transaction < self._since:
                        continue

                if self._on:
                    if date_of_transaction != self._on:
                        continue

                total_money = total_money + Money(event.data["value"])
                transactions.append(
                    {
                        "description": event.data["description"],
                        "value": str(Money(event.data["value"])),
                    }
                )

                # on="2020-01-01"

            return transactions, str(total_money)

        #  # Need something that reads a date in a string and loads it into a date
        #         # object and then allows to compare if it is > < or = than a date string
        #         d = datetime.strptime(str(t.date_of_movement), '%Y-%m-%d %H:%M:%S%z')
        #         _ = d

        # Construct the query
        sql_stmt = "SELECT description, value FROM balance"
        if self._since:
            sql_stmt += " WHERE date_of_movement >= :since"
        if self._on:
            sql_stmt += " WHERE date_of_movement = :on"

        # Bind parameters
        prepared_statement = text(sql_stmt)
        if self._since:
            prepared_statement = prepared_statement.bindparams(since=self._since)
        if self._on:
            prepared_statement = prepared_statement.bindparams(on=self._on)

        # Extract data
        rows = self._session.execute(prepared_statement)

        # Transform the data for output
        transactions = []
        for row in rows:
            transactions.append({"description": row[0], "value": row[1]})

        seller = self._seller
        total: float = 0.0

        for transaction in transactions:
            description = str(transaction["description"]).lower()
            value = float(transaction["value"])

            if not seller:
                total += value
                continue

            if seller and seller in description:
                total += value

        return transactions, total
