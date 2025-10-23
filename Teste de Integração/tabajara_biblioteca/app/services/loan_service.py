
from __future__ import annotations
from datetime import date, timedelta
from typing import Tuple
from ..models import User, Book, Loan
from ..repositories import InMemoryUserRepo, InMemoryBookRepo, InMemoryLoanRepo

MAX_LOANS = {"aluno": 3, "professor": 5}
DUE_DAYS = {"aluno": 14, "professor": 28}

class LoanError(Exception): ...
class NotFound(LoanError): ...
class ValidationError(LoanError): ...

class LoanService:
    def __init__(self, users: InMemoryUserRepo, books: InMemoryBookRepo, loans: InMemoryLoanRepo):
        self.users = users
        self.books = books
        self.loans = loans

    def loan_book(self, user_id: int, book_id: int, today: date | None = None) -> Loan:
        today = today or date.today()
        user = self.users.get(user_id)
        if not user:
            raise NotFound("User not found")
        book = self.books.get(book_id)
        if not book:
            raise NotFound("Book not found")
        if not book.is_available:
            raise ValidationError("Book not available")
        if self.loans.find_active_by_user_and_book(user_id, book_id):
            raise ValidationError("User already has this book on loan")
        active = self.loans.list_active_by_user(user_id)
        if len(active) >= MAX_LOANS[user.kind]:
            raise ValidationError("User reached loan limit")

        due = today + timedelta(days=DUE_DAYS[user.kind])
        loan = Loan(id=0, user_id=user_id, book_id=book_id, loan_date=today, due_date=due)
        self.loans.add(loan)
        book.available_copies -= 1
        return loan

    def return_book(self, loan_id: int, today: date | None = None) -> Loan:
        today = today or date.today()
        loan = self.loans.get(loan_id)
        if not loan:
            raise NotFound("Loan not found")
        if loan.returned:
            raise ValidationError("Loan already returned")
        book = self.books.get(loan.book_id)
        if not book:
            raise NotFound("Book not found for this loan")
        loan.returned = True
        loan.return_date = today
        book.available_copies += 1
        return loan
