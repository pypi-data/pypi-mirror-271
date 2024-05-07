import typing

import pastperfect
from sqlalchemy import text

from profitpulse.data.accounts import DIVESTED, PulseEvent, status_from_value
from profitpulse.data.views import View
from profitpulse.lib.money import Money


class PulseView(View):
    def __init__(self, session: typing.Any):
        self._session = session

    @property
    def data(self) -> typing.Any:
        sql_stmt = """SELECT name, status as name FROM account ORDER BY id ASC"""
        accounts = self._session.execute(text(sql_stmt))

        events = pastperfect.Events(self._session)

        results = []
        for account in accounts:
            account_name = account[0]
            status = account[1]
            account_details = ["n/a"] * 5
            invested = Money(0)
            current = Money(0)

            has_events = False
            for event in events:
                has_events = True
                if (
                    event.name == PulseEvent.ACCOUNT_REVALUE
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
            account_details[1] = status_from_value(status)
            if not has_events:
                results.append(account_details)
                continue

            account_details[2] = str(invested)
            account_details[3] = str(current)
            if status == DIVESTED:
                account_details[3] = "n/a"
            account_details[4] = str(current - invested)

            results.append(account_details)

        return results
