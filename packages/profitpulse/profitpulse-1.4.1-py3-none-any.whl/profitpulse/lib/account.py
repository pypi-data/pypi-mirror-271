from typing import List, Optional

from profitpulse.lib.account_name import AccountName
from profitpulse.lib.comment import Comment
from profitpulse.lib.money import Money


class AccountCantBeDeletedError(Exception):
    def __str__(self) -> str:
        return "Account can't be deleted"


class Account:
    def __init__(
        self,
        account_name: AccountName,
        closed: bool = False,
        balance: Optional[Money] = None,
        comment: Optional[Comment] = None,
    ):
        self._account_name = account_name
        self._closed = closed
        self._balance: Money = Money(0)
        self._comment: Optional[Comment] = comment
        if balance:
            self._balance = balance

        self._deposit_list: List[Money] = []

    def __repr__(self) -> str:
        return f"Account({self._account_name})"

    def snapshot(self, value: Money) -> None:
        self._balance = value

    @property
    def name(self) -> AccountName:
        return self._account_name

    @property
    def balance(self) -> Money:
        return self._balance

    def close(self) -> None:
        self._closed = True

    @property
    def closed(self) -> bool:
        return True if self._closed else False

    def deposit(self, amount: Money, comment: Optional[Comment] = None) -> None:
        if self.closed:
            return

        if self._balance + amount < Money(0):
            amount = Money(0)

        self._balance += amount
        self._comment = comment

        self._deposit_list.append(amount)

    def deposit_list(self) -> List[Money]:
        return self._deposit_list

    @property
    def last_comment(self) -> Optional[Comment]:
        return self._comment

    def prepare_deletion(self) -> None:
        if self._balance > Money(0):
            raise AccountCantBeDeletedError()
