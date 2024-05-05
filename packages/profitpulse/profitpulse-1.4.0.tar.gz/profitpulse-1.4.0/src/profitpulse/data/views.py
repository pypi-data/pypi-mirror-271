import abc

import pastperfect
from turbofan.database import text

from profitpulse.data import accounts as accounts_repository
from profitpulse.lib.money import Money


class View(abc.ABC):
    @property
    @abc.abstractmethod
    def data(self): ...


class AccountsView(View):
    def __init__(self, session) -> None:
        self._session = session

    @property
    def data(self):
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
                if not event.data.get("name") == account_name:
                    continue

                # account_details[1] = str(Money(event.data.get("balance")))

                total_balance = total_balance + Money(event.data.get("balance"))

            account_details[1] = str(total_balance)

            results.append(account_details)

        return results


class PulseView(View):
    def __init__(self, session):
        self._session = session

    @property
    def data(self):
        sql_stmt = """SELECT account.name as name FROM account ORDER BY id ASC"""
        accounts = self._session.execute(text(sql_stmt))

        events = pastperfect.Events(self._session)

        results = []
        total_balance = Money(0)
        for account in accounts:
            account_name = account[0]
            account_details = [account_name, "0.00", "N/A", "N/A"]
            for event in events:
                if not event.data.get("name") == account_name:
                    continue

                total_balance = total_balance + Money(event.data.get("balance"))

            account_details[1] = str(total_balance)

            results.append(account_details)

        return results


class TransactionsView(View):
    def __init__(self, session, seller=None, since=None, on=None) -> None:
        self._seller = seller.lower() if seller else None
        self._session = session
        self._since = since
        self._on = on

    @property
    def data(self):
        """
        The data resulting from the view execution.
        """

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
