from profitpulse.lib.account_name import AccountName


class AccountNotFoundError(Exception):
    def __init__(self, account_name: AccountName) -> None:
        self._account_name = account_name

    def __str__(self) -> str:
        return f"Could not find an account with name '{self._account_name}'"
