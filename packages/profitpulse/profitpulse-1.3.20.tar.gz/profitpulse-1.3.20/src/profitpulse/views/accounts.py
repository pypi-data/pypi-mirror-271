import pastperfect
from turbofan.database import text

from profitpulse.lib.money import Money
from profitpulse.repositories import accounts as accounts_repository
from profitpulse.views.views import View


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
