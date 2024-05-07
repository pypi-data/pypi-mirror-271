import pytest
from pastperfect import Event, Events
from turbofan.database import text

from profitpulse.data.accounts import ACTIVE, DIVESTED, PulseEvent
from profitpulse.data.pulse_view import PulseView


@pytest.mark.integration
def test_return_empty_list_when_no_data_was_found(tmp_db_session):
    pulse_view = PulseView(tmp_db_session)

    data = pulse_view.data

    assert data == []  # nosec


@pytest.mark.integration
def test_return_the_asset_name_when_an_asset_is_found(tmp_db_session):
    sql_stmt = "INSERT INTO account (name, status) VALUES (:name, :status)"
    prep_stmt = text(sql_stmt).bindparams(name="TheAccountName", status=DIVESTED)
    tmp_db_session.execute(prep_stmt)
    pulse_view = PulseView(tmp_db_session)

    data = pulse_view.data

    assert data == [["TheAccountName", "Divested", "n/a", "n/a", "n/a"]]  # nosec


@pytest.mark.integration
def test_should_return_the_asset_details(tmp_db_session):
    sql_stmt = "INSERT INTO account (name, status) VALUES (:name, :status)"
    prep_stmt = text(sql_stmt).bindparams(name="TheAccountName", status=ACTIVE)
    tmp_db_session.execute(prep_stmt)
    events = Events(tmp_db_session)
    events.append(
        Event(
            name=PulseEvent.MONEY_DEPOSIT,
            data={"name": "TheAccountName", "balance": 200},
        )
    )
    events.append(
        Event(
            name=PulseEvent.ACCOUNT_REVALUE,
            data={"name": "TheAccountName", "balance": 300},
        )
    )
    pulse_view = PulseView(tmp_db_session)

    data = pulse_view.data

    assert data == [["TheAccountName", "Active", "2.00", "3.00", "1.00"]]  # nosec
