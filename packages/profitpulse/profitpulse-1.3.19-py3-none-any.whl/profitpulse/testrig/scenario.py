# type: ignore
from typing import Optional

from typer.testing import CliRunner

from profitpulse.cli.main import app

runner = CliRunner(mix_stderr=False)


class CLIScenario:
    """
    Builds scenarios up on the tests can be run.
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __init__(self, *_, **__) -> None:
        self._app = app

    # Account management -----------------------------------------------------------------------------------------------

    def show_accounts(self):
        """
        Shows all the accounts and their current balance.
        """
        result = runner.invoke(self._app, ["accounts", "show"], catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec

        return result.stdout

    expect_accounts__first_usage = ""

    def open_account(self, account_name):
        """
        Opens a new account.
        """

        result = runner.invoke(
            self._app, ["accounts", "open", account_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec

    def close_account(self, account_name: str) -> None:
        """
        Closes an account.
        """
        result = runner.invoke(
            self._app, ["accounts", "close", account_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec
        assert result.stdout == "", result.stdout  # nosec

    def delete_account(self, account_name: str) -> None:
        """
        Deletes an account.
        """
        result = runner.invoke(
            self._app, ["accounts", "delete", account_name], catch_exceptions=False
        )
        assert result.exit_code == 0, result.stderr  # nosec

    # Money transactions  ----------------------------------------------------------------------------------------------

    def deposit(
        self, cent_amount: int, account_name: str, comment: Optional[str] = None
    ) -> None:
        args = ["deposit", str(cent_amount), account_name]
        if comment:
            args.append("--comment")
            args.append(comment)
        result = runner.invoke(self._app, args, catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec

    def withdraw(self, cent_amount: int, account_name: str) -> None:
        result = runner.invoke(
            self._app,
            ["withdraw", str(cent_amount), account_name],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec

    def transfer(self, amount: int, from_account: str, to_account: str):
        result = runner.invoke(
            self._app,
            ["transfer", str(amount), from_account, to_account],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    # Reports ----------------------------------------------------------------------------------------------------------

    def pulse(self):
        """
        Shows a global view of the user finances.
        """

        result = runner.invoke(self._app, ["pulse"], catch_exceptions=False)

        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    # I don't remember what these are .... facepalm --------------------------------------------------------------------

    def report(self, seller: Optional[str] = None, month: Optional[int] = None):
        cmd = ["report"]
        if seller:
            cmd.append("--seller")
            cmd.append(seller)

        if month:
            cmd.append("--since")
            cmd.append(f"2023-{month}-01")

        result = runner.invoke(self._app, cmd, catch_exceptions=False)
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout

    @property
    def current_month(self) -> str:
        """
        Returns the current month of the imported transactions.
        """
        # This is one of the months defined in the fixture file comprovativo_cgd.csv
        return "8"

    def import_transactions(self, transactions_file: str, account_name: str):
        result = runner.invoke(
            self._app,
            ["import", str(transactions_file), account_name],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.stderr  # nosec
        return result.stdout
