
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

VALID_USER_KINDS = {"aluno", "professor"}

@dataclass
class User:
    id: int
    name: str
    kind: str  # "aluno" or "professor"

    def __post_init__(self):
        if self.kind not in VALID_USER_KINDS:
            raise ValueError("kind must be 'aluno' or 'professor'")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "kind": self.kind}

    @staticmethod
    def from_dict(d: dict) -> "User":
        return User(id=d["id"], name=d["name"], kind=d["kind"])


@dataclass
class Book:
    id: int
    title: str
    author: str
    total_copies: int
    available_copies: int

    def __post_init__(self):
        if self.total_copies < 0 or self.available_copies < 0:
            raise ValueError("copies cannot be negative")
        if self.available_copies > self.total_copies:
            raise ValueError("available_copies cannot exceed total_copies")
        if not self.title or not self.title.strip():
            raise ValueError("title is required")

    @property
    def is_available(self) -> bool:
        return self.available_copies > 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "is_available": self.is_available,
        }

    @staticmethod
    def from_dict(d: dict) -> "Book":
        return Book(
            id=d["id"],
            title=d["title"],
            author=d["author"],
            total_copies=d["total_copies"],
            available_copies=d["available_copies"],
        )


@dataclass
class Loan:
    id: int
    user_id: int
    book_id: int
    loan_date: date
    due_date: date
    returned: bool = False
    return_date: Optional[date] = None

    def __post_init__(self):
        if self.due_date <= self.loan_date:
            raise ValueError("due_date must be after loan_date")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "returned": self.returned,
            "return_date": self.return_date.isoformat() if self.return_date else None,
        }

    @staticmethod
    def from_dict(d: dict) -> "Loan":
        from datetime import date
        return Loan(
            id=d["id"],
            user_id=d["user_id"],
            book_id=d["book_id"],
            loan_date=date.fromisoformat(d["loan_date"]),
            due_date=date.fromisoformat(d["due_date"]),
            returned=d.get("returned", False),
            return_date=date.fromisoformat(d["return_date"]) if d.get("return_date") else None,
        )
