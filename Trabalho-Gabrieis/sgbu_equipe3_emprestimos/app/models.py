
from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from typing import Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    matricula = db.Column(db.String(40), unique=True, nullable=False)
    user_type = db.Column(db.String(30), default="aluno")  # aluno, professor, staff

    def __repr__(self) -> str:
        return f"<User {self.id} {self.name}>"

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Book {self.id} {self.title} avail={self.available}>"

class Loan(db.Model):
    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", backref=db.backref("loans", lazy=True))
    book = db.relationship("Book", backref=db.backref("loans", lazy=True))

    @staticmethod
    def make_due_date(days: int | None) -> datetime:
        days = days if days and days > 0 else 7
        return datetime.utcnow() + timedelta(days=days)

    @property
    def is_open(self) -> bool:
        return self.return_date is None

    def register_return(self) -> None:
        if self.return_date is not None:
            raise ValueError("Empréstimo já devolvido.")
        self.return_date = datetime.utcnow()
        # book becomes available again
        if self.book is None:
            raise ValueError("Livro associado não encontrado.")
        self.book.available = True
