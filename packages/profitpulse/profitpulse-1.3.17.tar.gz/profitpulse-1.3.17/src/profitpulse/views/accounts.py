from turbofan.database import text

from profitpulse.lib.money import Money
from profitpulse.repositories import accounts
from profitpulse.views.views import View


class AccountsView(View):
    def __init__(self, session) -> None:
        self._session = session

    @property
    def data(self):
        sql_stmt = """
          SELECT account.name as name,
                 COALESCE(balance.value , 0) as balance,
                 account.status,
                 balance.description
            FROM account
       LEFT JOIN balance
              ON account.id = balance.account_id
        """
        rows = self._session.execute(text(sql_stmt))
        rows = list(rows)

        result = []
        for row in rows:
            # Name, Balance, Status, Comment
            result.append(
                [
                    row[0],
                    str(Money(row[1])),
                    "Open" if row[2] == accounts.OPEN else "Closed",
                    row[3] if row[3] else "",
                ]
            )

        return result
