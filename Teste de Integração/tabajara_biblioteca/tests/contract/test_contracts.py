
import pytest
from app.models import User, Book, Loan
from datetime import date

def test_user_serialization_contract_keys():
    u = User(id=1, name="Ana", kind="aluno")
    d = u.to_dict()
    assert set(d.keys()) == {"id","name","kind"}

def test_book_serialization_includes_is_available():
    b = Book(id=1, title="Clean", author="M", total_copies=2, available_copies=1)
    d = b.to_dict()
    assert "is_available" in d and isinstance(d["is_available"], bool)

def test_loan_serialization_dates_are_isoformat():
    l = Loan(id=1, user_id=1, book_id=2, loan_date=date(2025,1,1), due_date=date(2025,1,5))
    d = l.to_dict()
    assert d["loan_date"] == "2025-01-01"
    assert d["due_date"] == "2025-01-05"

def test_required_fields_validation():
    with pytest.raises(ValueError):
        User(id=1, name="   ", kind="aluno")
    with pytest.raises(ValueError):
        Book(id=1, title="", author="A", total_copies=1, available_copies=1)

def test_roundtrip_from_to_dict():
    u = User.from_dict({"id":2,"name":"Bia","kind":"professor"})
    b = Book.from_dict({"id":3,"title":"X","author":"Y","total_copies":1,"available_copies":1})
    l = Loan.from_dict({"id":4,"user_id":u.id,"book_id":b.id,"loan_date":"2025-01-01","due_date":"2025-01-10","returned":False})
    assert u.kind == "professor"
    assert b.title == "X"
    assert l.due_date.year == 2025
