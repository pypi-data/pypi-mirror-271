from typing import Optional

from turbofan.database import text


class DatabaseScenario:
    def __init__(self, session):
        self.session = session
        self.account_id = None

    def log_transaction(self, description, value, date_of_movement, origin, account_id):
        sql_statement = """
            INSERT INTO balance (description, value, date_of_movement, origin, account_id)
                 VALUES (:description, :value, :date_of_movement, :origin, :account_id)
        """

        prepared_statement = text(sql_statement).bindparams(
            description=description,
            value=value,
            date_of_movement=date_of_movement,
            origin=origin,
            account_id=account_id,
        )

        self.session.execute(prepared_statement)
        return self

    def open_account(self, name):
        sql_statement = "INSERT INTO account (name)VALUES (:name)"
        prepared_statement = text(sql_statement).bindparams(name=name)
        result = self.session.execute(prepared_statement)
        self.account_id = result.lastrowid
        return self

    def deposit(
        self,
        cent_amount: int,
        account_name: str,
        comment: Optional[str] = None,
    ):
        sql_statement = """
            INSERT INTO balance (account_id, value, description)
                 VALUES ((SELECT id FROM account WHERE name = :name), :value, :comment)
        """
        prepared_statement = text(sql_statement).bindparams(
            name=str(account_name),
            value=str(cent_amount),
            comment=str(comment) if comment else None,
        )
        self.session.execute(prepared_statement)
