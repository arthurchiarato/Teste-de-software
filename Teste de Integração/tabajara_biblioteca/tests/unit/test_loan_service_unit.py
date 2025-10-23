
from datetime import date, timedelta
import pytest
from app.models import User, Book
from app.repositories import InMemoryUserRepo, InMemoryBookRepo, InMemoryLoanRepo
from app.services.loan_service import LoanService, ValidationError, NotFound, MAX_LOANS, DUE_DAYS

def make_ctx():
    users = InMemoryUserRepo()
    books = InMemoryBookRepo()
    loans = InMemoryLoanRepo()
    svc = LoanService(users, books, loans)
    return users, books, loans, svc

def seed_basic(users, books):
    users.add(User(id=1, name="Ana", kind="aluno"))
    users.add(User(id=2, name="Prof. B", kind="professor"))
    books.add(Book(id=10, title="Clean Code", author="Martin", total_copies=2, available_copies=2))

def test_loan_success_when_available():
    users, books, loans, svc = make_ctx()
    seed_basic(users, books)
    loan = svc.loan_book(user_id=1, book_id=10, today=date(2025,1,1))
    assert loan.id == 1
    assert books.get(10).available_copies == 1

def test_cannot_loan_when_book_not_found():
    users, books, loans, svc = make_ctx()
    users.add(User(id=1, name="Ana", kind="aluno"))
    with pytest.raises(NotFound):
        svc.loan_book(1, 999)

def test_cannot_loan_when_user_not_found():
    users, books, loans, svc = make_ctx()
    books.add(Book(id=10, title="CC", author="M", total_copies=1, available_copies=1))
    with pytest.raises(NotFound):
        svc.loan_book(123, 10)

def test_cannot_loan_when_unavailable():
    users, books, loans, svc = make_ctx()
    users.add(User(id=1, name="Ana", kind="aluno"))
    books.add(Book(id=10, title="CC", author="M", total_copies=1, available_copies=0))
    with pytest.raises(ValidationError):
        svc.loan_book(1, 10)

def test_cannot_duplicate_active_loan_same_book():
    users, books, loans, svc = make_ctx()
    seed_basic(users, books)
    svc.loan_book(1, 10, today=date(2025,1,1))
    with pytest.raises(ValidationError):
        svc.loan_book(1, 10, today=date(2025,1,2))

def test_respects_user_limit_aluno():
    users, books, loans, svc = make_ctx()
    users.add(User(id=1, name="Ana", kind="aluno"))
    for i in range(3):
        books.add(Book(id=100+i, title=f"B{i}", author="X", total_copies=1, available_copies=1))
        svc.loan_book(1, 100+i, today=date(2025,1,1))
    books.add(Book(id=200, title="Extra", author="Y", total_copies=1, available_copies=1))
    with pytest.raises(ValidationError):
        svc.loan_book(1, 200, today=date(2025,1,1))

def test_due_date_for_aluno_and_professor():
    users, books, loans, svc = make_ctx()
    users.add(User(id=1, name="Ana", kind="aluno"))
    users.add(User(id=2, name="Prof", kind="professor"))
    books.add(Book(id=10, title="X", author="A", total_copies=2, available_copies=2))
    start = date(2025,1,1)
    loan1 = svc.loan_book(1, 10, today=start)
    loan2 = svc.loan_book(2, 10, today=start)
    assert loan1.due_date == start + timedelta(days=DUE_DAYS["aluno"])
    assert loan2.due_date == start + timedelta(days=DUE_DAYS["professor"])

def test_return_increases_stock():
    users, books, loans, svc = make_ctx()
    seed_basic(users, books)
    loan = svc.loan_book(1, 10, today=date(2025,1,1))
    svc.return_book(loan.id, today=date(2025,1,5))
    assert books.get(10).available_copies == 2

def test_cannot_return_twice():
    users, books, loans, svc = make_ctx()
    seed_basic(users, books)
    loan = svc.loan_book(1, 10, today=date(2025,1,1))
    svc.return_book(loan.id, today=date(2025,1,5))
    import pytest
    with pytest.raises(ValidationError):
        svc.return_book(loan.id)

def test_models_validation_and_properties():
    from app.models import Book, User, Loan
    from datetime import date, timedelta
    b = Book(id=1, title="T", author="A", total_copies=1, available_copies=1)
    assert b.is_available
    u = User(id=5, name="N", kind="aluno")
    loan = Loan(id=9, user_id=u.id, book_id=b.id, loan_date=date(2025,1,1), due_date=date(2025,1,2))
    assert loan.due_date > loan.loan_date
