
import pytest
from datetime import date
from app.models import User, Book
from app.repositories import InMemoryUserRepo, InMemoryBookRepo, InMemoryLoanRepo
from app.services.loan_service import LoanService, ValidationError

def make_world():
    users = InMemoryUserRepo()
    books = InMemoryBookRepo()
    loans = InMemoryLoanRepo()
    svc = LoanService(users, books, loans)
    return users, books, loans, svc

def test_full_flow_user_book_loan_and_return():
    users, books, loans, svc = make_world()
    users.add(User(id=1, name="Ana", kind="aluno"))
    books.add(Book(id=10, title="Clean Code", author="M", total_copies=1, available_copies=1))
    loan = svc.loan_book(1, 10, today=date(2025,1,1))
    assert books.get(10).available_copies == 0
    svc.return_book(loan.id, today=date(2025,1,3))
    assert books.get(10).available_copies == 1

def test_two_users_contend_for_last_copy():
    users, books, loans, svc = make_world()
    users.add(User(id=1, name="Ana", kind="aluno"))
    users.add(User(id=2, name="Bia", kind="aluno"))
    books.add(Book(id=10, title="Clean Code", author="M", total_copies=1, available_copies=1))
    svc.loan_book(1, 10, today=date(2025,1,1))
    with pytest.raises(ValidationError):
        svc.loan_book(2, 10, today=date(2025,1,1))

def test_integration_uses_all_repositories():
    users, books, loans, svc = make_world()
    users.add(User(id=1, name="Ana", kind="aluno"))
    books.add(Book(id=1, title="X", author="A", total_copies=2, available_copies=2))
    loan = svc.loan_book(1, 1, today=date(2025,1,1))
    assert loans.get(loan.id) is not None
    assert books.get(1).available_copies == 1

def test_return_requires_existing_book_reference():
    users, books, loans, svc = make_world()
    users.add(User(id=1, name="Ana", kind="aluno"))
    books.add(Book(id=1, title="X", author="A", total_copies=1, available_copies=1))
    loan = svc.loan_book(1, 1, today=date(2025,1,1))
    # remove the book to simulate bad integration state
    books._data.pop(1)
    from app.services.loan_service import NotFound
    with pytest.raises(NotFound):
        svc.return_book(loan.id)

def test_limit_enforced_across_integration():
    users, books, loans, svc = make_world()
    users.add(User(id=1, name="Ana", kind="aluno"))
    for i in range(3):
        books.add(Book(id=100+i, title=f"B{i}", author="Z", total_copies=1, available_copies=1))
        svc.loan_book(1, 100+i, today=date(2025,1,1))
    books.add(Book(id=200, title="Extra", author="Z", total_copies=1, available_copies=1))
    with pytest.raises(ValidationError):
        svc.loan_book(1, 200, today=date(2025,1,2))
