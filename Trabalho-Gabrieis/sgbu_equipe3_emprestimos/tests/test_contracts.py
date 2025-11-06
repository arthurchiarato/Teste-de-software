
from app.models import db, User, Book, Loan
from datetime import datetime

def test_contract_user_fields(app):
    with app.app_context():
        u = User(name="Teste", matricula="C1", user_type="aluno")
        db.session.add(u); db.session.commit()
        assert u.id is not None
        assert isinstance(u.name, str) and isinstance(u.matricula, str)

def test_contract_book_fields(app):
    with app.app_context():
        b = Book(title="Titulo", author="Autor", available=True)
        db.session.add(b); db.session.commit()
        assert isinstance(b.available, bool)

def test_contract_loan_fields(app):
    with app.app_context():
        u = User(name="T", matricula="C2", user_type="aluno")
        b = Book(title="T", author="A", available=True)
        db.session.add_all([u,b]); db.session.commit()
        l = Loan(user_id=u.id, book_id=b.id, due_date=Loan.make_due_date(7))
        db.session.add(l); db.session.commit()
        assert isinstance(l.loan_date, datetime)
        assert l.return_date is None

def test_contract_foreign_keys(app):
    with app.app_context():
        u = User(name="T2", matricula="C3", user_type="aluno")
        b = Book(title="T2", author="A2", available=True)
        db.session.add_all([u,b]); db.session.commit()
        l = Loan(user_id=u.id, book_id=b.id, due_date=Loan.make_due_date(7))
        db.session.add(l); db.session.commit()
        assert l.user.id == u.id and l.book.id == b.id

def test_contract_serialization_shape(client, app):
    with app.app_context():
        u = User(name="TT", matricula="C4", user_type="aluno")
        b = Book(title="TB", author="AB", available=True)
        db.session.add_all([u,b]); db.session.commit()
        loan_id = client.post("/api/loans", json={"user_id": u.id, "book_id": b.id}).get_json()["id"]
        item = client.get("/api/loans").get_json()[0]
        assert {"id","user","book","loan_date","due_date","return_date"} <= set(item.keys())
