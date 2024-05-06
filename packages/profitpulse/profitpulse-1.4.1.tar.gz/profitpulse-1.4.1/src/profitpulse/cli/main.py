"""
CLI entry points for Typer (https://typer.tiangolo.com/) made CLI.
"""

from datetime import datetime
from importlib.metadata import version as get_version
from pathlib import Path
from typing import Optional

import typer

from profitpulse.cli.adapters import (
    close_account,
    database_path,
    delete_account,
    deposit,
    import_file,
    open_account,
    pulse,
    report,
    reset,
    show_accounts,
    snapshot,
    transfer,
)
from profitpulse.infrastructure.migrations import migrate_database  # type: ignore

profitpulse_app = typer.Typer(
    add_completion=False,
    help="Profitpulse helps you manage your personal finances.",
)

profitpulse_accounts_app = typer.Typer()
profitpulse_app.add_typer(
    profitpulse_accounts_app,
    name="accounts",
    help="Handles accounts",
)


@profitpulse_app.command(name="version", help="Shows the current profitpulse version")
def version() -> None:
    migrate_database(database_path)
    typer.echo(get_version("profitpulse"))


@profitpulse_app.command(name="pulse", help="Show's the health of your wealth")
def pulse_() -> None:
    migrate_database(database_path)
    pulse()


@profitpulse_app.command(
    name="snapshot", help="Save the current balance for an account"
)
def snapshot_(
    cent_amount: int = typer.Argument(
        0, help="Amount to deposit in cents", metavar="AMOUNT"
    ),
    account_name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
) -> None:
    migrate_database(database_path)
    snapshot(cent_amount, account_name)


@profitpulse_app.command(name="import", help="Import transactions for expense tracking")
def import_(
    file_path: Path,
    account_name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
) -> None:
    migrate_database(database_path)
    import_file(file_path, account_name)


@profitpulse_app.command(name="report", help="Builds reports according to filters")
def report_(
    seller: Optional[str] = typer.Option(default="", help="Filters report by Seller"),
    since: Optional[datetime] = typer.Option(
        default=None, help="Show report since specified date"
    ),
    on: Optional[datetime] = typer.Option(
        default=None, help="Show report on specified date"
    ),
) -> None:
    migrate_database(database_path)
    report(seller, since, on)


@profitpulse_app.command(name="reset", help="Deletes all information in profitpulse")
def reset_() -> None:
    delete_information = typer.confirm(
        "Are you sure you want to delete all financial information ?"
    )
    migrate_database(database_path)
    if not delete_information:
        raise typer.Abort()

    reset()


@profitpulse_app.command(name="deposit", help="Deposits money into an account")
def deposit_(
    cent_amount: int = typer.Argument(
        0, help="Amount to deposit in cents", metavar="AMOUNT"
    ),
    account_name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
    comment: Optional[str] = typer.Option(
        default=None, help="Comment to add to the transaction"
    ),
) -> None:
    migrate_database(database_path)
    deposit(cent_amount, account_name, comment=comment)


@profitpulse_app.command(name="withdraw", help="Withdraws money from an account")
def withdraw_(
    cent_amount: int = typer.Argument(
        0, help="Amount to withdraw in cents", metavar="AMOUNT"
    ),
    account_name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
) -> None:
    migrate_database(database_path)
    deposit(-cent_amount, account_name)


@profitpulse_app.command(name="transfer", help="Transfers money between accounts")
def transfer_(
    cent_amount: int = typer.Argument(
        0, help="Amount to transfer in cents", metavar="AMOUNT"
    ),
    from_account_name: str = typer.Argument(
        "", help="Name of the account to transfer from", metavar='"ACCOUNT NAME"'
    ),
    to_account_name: str = typer.Argument(
        "", help="Name of the account to transfer to", metavar='"ACCOUNT NAME"'
    ),
) -> None:
    migrate_database(database_path)
    transfer(cent_amount, from_account_name, to_account_name)


@profitpulse_accounts_app.command(name="show", help="Shows existing accounts")
def show() -> None:
    migrate_database(database_path)
    show_accounts()


@profitpulse_accounts_app.command(name="open", help="Opens a new account")
def open_(
    name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
) -> None:
    migrate_database(database_path)
    open_account(name)


@profitpulse_accounts_app.command(name="close", help="Closes an account")
def close_(
    name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
) -> None:
    migrate_database(database_path)
    close_account(name)


@profitpulse_accounts_app.command(name="delete", help="Deletes an account")
def delete_(
    name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
) -> None:
    migrate_database(database_path)
    delete_account(name)
