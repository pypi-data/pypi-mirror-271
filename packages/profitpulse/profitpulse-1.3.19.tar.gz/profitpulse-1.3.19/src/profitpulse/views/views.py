import abc

import pastperfect
from turbofan.database import text

from profitpulse.lib.money import Money


class View(abc.ABC):
    @property
    def data(self):
        return []


class PulseView(View):
    def __init__(self, session):
        self._session = session

    @property
    def data(self):
        sql_stmt = """SELECT account.name as name FROM account ORDER BY id ASC"""
        accounts = self._session.execute(text(sql_stmt))

        events = pastperfect.Events(self._session)

        results = []
        for account in accounts:
            account_name = account[0]
            account_details = [account_name, "0.00", "N/A", "N/A"]
            for event in events:
                if not event.data.get("name") == account_name:
                    continue

                account_details[1] = str(Money(event.data.get("balance")))

            results.append(account_details)

        return results
