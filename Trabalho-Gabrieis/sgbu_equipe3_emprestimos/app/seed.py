
from .models import db, User, Book

def seed_example_data():
    if not User.query.first():
        u1 = User(name="Alice Silva", matricula="A12345", user_type="aluno")
        u2 = User(name="Prof. Bruno", matricula="P67890", user_type="professor")
        db.session.add_all([u1, u2])
    if not Book.query.first():
        b1 = Book(title="Clean Code", author="Robert C. Martin", available=True)
        b2 = Book(title="Introdução a Algoritmos", author="Cormen", available=True)
        b3 = Book(title="Arquitetura de Software", author="Bass", available=True)
        db.session.add_all([b1, b2, b3])
    db.session.commit()
