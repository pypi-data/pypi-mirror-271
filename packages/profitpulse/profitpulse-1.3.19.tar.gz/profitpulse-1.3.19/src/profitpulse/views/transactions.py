import typing

from turbofan.database import text

from profitpulse.views.views import View


class DatabaseSessioner(typing.Protocol):
    def scalars(*_):
        pass  # pragma: no cover


class ViewTransactions(View):
    def __init__(
        self, session: DatabaseSessioner, seller=None, since=None, on=None
    ) -> None:
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

        # Transform the data for ouput
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
