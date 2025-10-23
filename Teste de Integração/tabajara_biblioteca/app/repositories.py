
from __future__ import annotations
from typing import Dict, List, Optional
from .models import User, Book, Loan

class InMemoryUserRepo:
    def __init__(self):
        self._data: Dict[int, User] = {}

    def add(self, user: User) -> None:
        self._data[user.id] = user

    def get(self, user_id: int) -> Optional[User]:
        return self._data.get(user_id)

    def list_all(self) -> List[User]:
        return list(self._data.values())


class InMemoryBookRepo:
    def __init__(self):
        self._data: Dict[int, Book] = {}

    def add(self, book: Book) -> None:
        self._data[book.id] = book

    def get(self, book_id: int) -> Optional[Book]:
        return self._data.get(book_id)

    def list_all(self) -> List[Book]:
        return list(self._data.values())


class InMemoryLoanRepo:
    def __init__(self):
        self._data: Dict[int, Loan] = {}
        self._next_id = 1

    def add(self, loan: Loan) -> Loan:
        if loan.id == 0:
            loan.id = self._next_id
            self._next_id += 1
        self._data[loan.id] = loan
        return loan

    def get(self, loan_id: int) -> Optional[Loan]:
        return self._data.get(loan_id)

    def list_all(self) -> List[Loan]:
        return list(self._data.values())

    def list_active_by_user(self, user_id: int):
        return [l for l in self._data.values() if l.user_id == user_id and not l.returned]

    def find_active_by_user_and_book(self, user_id: int, book_id: int) -> Optional[Loan]:
        for l in self._data.values():
            if l.user_id == user_id and l.book_id == book_id and not l.returned:
                return l
        return None
