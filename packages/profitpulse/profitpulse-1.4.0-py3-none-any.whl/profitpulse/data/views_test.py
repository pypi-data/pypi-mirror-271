from typing import Optional

import pytest
from turbofan.database import text

from profitpulse.data.views import AccountsView, TransactionsView
from profitpulse.lib.money import Money


class TestAccountsView:
    @pytest.mark.integration
    def test_return_no_data_when_no_accounts(self, tmp_db_session):
        assert AccountsView(tmp_db_session).data == []  # nosec

    @pytest.mark.integration
    def test_return_one_account_when_one_account_exists(self, tmp_db_session):
        DatabaseScenario(tmp_db_session).open_account(name="TheAccountName")
        assert AccountsView(tmp_db_session).data == [  # nosec
            ["TheAccountName", str(Money(0)), "Closed", ""]
        ]


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


class TestTransactionsView:

    @pytest.mark.integration
    def test_shown_no_transactions_on_empty_database(self, tmp_db_session):
        transactions, total = TransactionsView(tmp_db_session).data

        assert not transactions  # nosec
        assert not total  # nosec

    @pytest.mark.integration
    def test_show_one_transaction_when_one_is_available(self, tmp_db_session):
        """
        Given a database with one transaction
        When the view is executed
        Then the transaction is shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_account("TheAccountName")
        scenario.log_transaction("foo", 1, "2020-01-01", "foo", scenario.account_id)

        transactions, total = TransactionsView(tmp_db_session).data

        assert transactions == [{"description": "foo", "value": 1}]  # nosec
        assert total == 1  # nosec

    @pytest.mark.integration
    def test_show_multiple_transactions_when_more_than_one_is_available(
        self, tmp_db_session
    ):
        """
        Given a database with multiple transactions
        When the view is executed
        Then the transactions are shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_account("TheAccountName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.account_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-01",
            "foo",
            scenario.account_id,
        )

        transactions, total = TransactionsView(tmp_db_session).data

        assert transactions == [  # nosec
            {"description": "foo", "value": 1},
            {"description": "bar", "value": 2},
        ]
        assert total == 3  # nosec

    @pytest.mark.integration
    def test_show_transactions_since_a_given_date(self, tmp_db_session):
        """
        Given a database with multiple transactions
        When the view is executed with a since date
        Then the transactions since the given date are shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_account("TheAccountName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.account_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-02",
            "foo",
            scenario.account_id,
        )

        transactions, total = TransactionsView(tmp_db_session, since="2020-01-02").data

        assert transactions == [{"description": "bar", "value": 2}]  # nosec
        assert total == 2  # nosec

    @pytest.mark.integration
    def test_show_transactions_on_a_given_date(self, tmp_db_session):
        """
        Given a database with multiple transactions
        When the view is executed with a on date
        Then the transactions on the given date are shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_account("TheAccountName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.account_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-02",
            "foo",
            scenario.account_id,
        )

        transactions, total = TransactionsView(tmp_db_session, on="2020-01-01").data

        assert transactions == [{"description": "foo", "value": 1.0}]  # nosec
        assert total == 1.0  # nosec

    @pytest.mark.integration
    def test_show_total_for_a_specific_seller(self, tmp_db_session):
        """
        Given a database with multiple transactions
        When the view is executed with a seller
        Then the total for the given seller is shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_account("TheAccountName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.account_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-02",
            "foo",
            scenario.account_id,
        )

        transactions, total = TransactionsView(tmp_db_session, seller="foo").data

        assert total == 1.0  # nosec
