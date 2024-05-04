"""
CLI entry points for Typer (https://typer.tiangolo.com/) made CLI.
"""

from datetime import datetime
from importlib.metadata import version as get_version
from pathlib import Path
from typing import Optional

import typer

from profitpulse.cli.cli_adapters import (
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
    transfer,
)
from profitpulse.infrastructure.migrations import migrate_database

app = typer.Typer(
    add_completion=False,
    help="Profitpulse helps you manage your personal finances.",
)


@app.command(name="version", help="Shows current version")
def version():
    migrate_database(database_path)
    typer.echo(get_version("profitpulse"))


@app.command(name="pulse", help="Show the health of your savings")
def pulse_():
    pulse()


@app.command(name="import", help="Import transactions for expense tracking")
def import_(
    file_path: Path,
    account_name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
):
    migrate_database(database_path)
    import_file(file_path, account_name)


@app.command(name="report", help="Builds reports according to filters")
def report_(
    seller: Optional[str] = typer.Option(default="", help="Filters report by Seller"),
    since: Optional[datetime] = typer.Option(
        default=None, help="Show report since specified date"
    ),
    on: Optional[datetime] = typer.Option(
        default=None, help="Show report on specified date"
    ),
):
    migrate_database(database_path)
    report(seller, since, on)


@app.command(
    name="reset",
    help="Deletes all information in profitpulse",
)
def reset_():
    delete_information = typer.confirm(
        "Are you sure you want to delete all financial information ?"
    )
    migrate_database(database_path)
    if not delete_information:
        raise typer.Abort()

    reset()


@app.command(name="deposit", help="Deposits money into an account")
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
):
    migrate_database(database_path)
    deposit(cent_amount, account_name, comment=comment)


@app.command(name="withdraw", help="Withdraws money from an account")
def withdraw_(
    cent_amount: int = typer.Argument(
        0, help="Amount to withdraw in cents", metavar="AMOUNT"
    ),
    account_name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
):
    migrate_database(database_path)
    deposit(-cent_amount, account_name)


@app.command(name="transfer", help="Transfers money between accounts")
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
):
    migrate_database(database_path)
    transfer(cent_amount, from_account_name, to_account_name)


accounts_app = typer.Typer()
app.add_typer(accounts_app, name="accounts", help="Handles accounts")


@accounts_app.command(name="show", help="Shows existing accounts")
def show():
    migrate_database(database_path)
    show_accounts()


@accounts_app.command(name="open", help="Opens a new account")
def open_(
    name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
):
    migrate_database(database_path)
    open_account(name)


@accounts_app.command(name="close", help="Closes an account")
def close_(
    name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
):
    migrate_database(database_path)
    close_account(name)


@accounts_app.command(name="delete", help="Deletes an account")
def delete_(
    name: str = typer.Argument(
        "", help="Name of the account", metavar='"ACCOUNT NAME"'
    ),
):
    migrate_database(database_path)
    delete_account(name)
