import pytest

from profitpulse.lib.money import Money
from profitpulse.views.accounts import AccountsView
from profitpulse.views.cenas import DatabaseScenario


@pytest.mark.integration
def test_return_no_data_when_no_accounts(tmp_db_session):
    assert AccountsView(tmp_db_session).data == []  # nosec


@pytest.mark.integration
def test_return_one_account_when_one_account_exists(tmp_db_session):
    DatabaseScenario(tmp_db_session).open_account(name="TheAccountName")
    assert AccountsView(tmp_db_session).data == [  # nosec
        ["TheAccountName", str(Money(0)), "Closed", ""]
    ]
