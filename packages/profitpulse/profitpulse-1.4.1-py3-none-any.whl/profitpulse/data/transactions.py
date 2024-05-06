import typing

import pastperfect
from turbofan.database import text

from profitpulse.data.accounts import PulseEvent
from profitpulse.lib.account_name import AccountName
from profitpulse.lib.transaction import Transaction
from profitpulse.services.import_transactions import (
    ImportTransactionsTransactionCollector,
)


class Transactions(ImportTransactionsTransactionCollector):
    def __init__(self, session: typing.Any) -> None:
        self._session = session

    def append(self, t: Transaction, account_name: AccountName) -> None:
        """
        Append a transaction to the repository.
        """

        # Get the account id by account name
        sql_statement = """
            SELECT id
              FROM account
             WHERE name = :name
        """
        prepared_statement = text(sql_statement).bindparams(name=str(account_name))
        result = self._session.execute(prepared_statement)
        account_id = result.fetchone()[0]

        # Insert the transaction
        sql_statement = """
            INSERT INTO balance (date_of_movement, description, value, origin, account_id)
                 VALUES (:date_of_movement, :description, :value, :origin, :account_id)
        """
        prepared_statement = text(sql_statement).bindparams(
            date_of_movement=str(t.date_of_movement),
            description=t.description,
            value=t.value,
            origin=t.origin,
            account_id=account_id,
        )
        self._session.execute(prepared_statement)

        events = pastperfect.Events(self._session)
        events.append(
            pastperfect.Event(
                name=PulseEvent.TRANSACTION_IMPORTED,
                data={
                    "value": int(str(t.value).replace(".", "")),
                    "date": str(
                        t.date_of_movement.date()
                    ),  # TODO: should not need date()
                    "description": t.description,
                },
            )
        )
