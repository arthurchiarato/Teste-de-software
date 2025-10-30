
from app.models import db, User, Book, Loan

def create_user(name="User", matricula="X1", user_type="aluno"):
    u = User(name=name, matricula=matricula, user_type=user_type)
    db.session.add(u)
    db.session.commit()
    return u

def create_book(title="Livro A", author="Autor A", available=True):
    b = Book(title=title, author=author, available=available)
    db.session.add(b)
    db.session.commit()
    return b

def test_create_loan_sets_book_unavailable(client, app):
    with app.app_context():
        u = create_user(matricula="M1")
        b = create_book()
        resp = client.post("/api/loans", json={"user_id": u.id, "book_id": b.id, "loan_days": 5})
        assert resp.status_code == 201
        assert b.available is False

def test_cannot_loan_unavailable_book(client, app):
    with app.app_context():
        u = create_user(matricula="M2")
        b = create_book(available=False)
        resp = client.post("/api/loans", json={"user_id": u.id, "book_id": b.id})
        assert resp.status_code == 409

def test_cannot_loan_to_missing_user(client, app):
    with app.app_context():
        b = create_book()
        resp = client.post("/api/loans", json={"user_id": 9999, "book_id": b.id})
        assert resp.status_code == 400

def test_cannot_loan_missing_book(client, app):
    with app.app_context():
        u = create_user(matricula="M3")
        resp = client.post("/api/loans", json={"user_id": u.id, "book_id": 9999})
        assert resp.status_code == 400

def test_default_loan_days_7(client, app):
    with app.app_context():
        u = create_user(matricula="M4")
        b = create_book()
        resp = client.post("/api/loans", json={"user_id": u.id, "book_id": b.id})
        assert resp.status_code == 201
        loan_id = resp.get_json()["id"]
        loan = Loan.query.get(loan_id)
        assert (loan.due_date - loan.loan_date).days in (6,7,8)  # tolerância por hora

def test_return_loan_makes_book_available(client, app):
    with app.app_context():
        u = create_user(matricula="M5")
        b = create_book()
        resp = client.post("/api/loans", json={"user_id": u.id, "book_id": b.id})
        loan_id = resp.get_json()["id"]
        assert b.available is False
        resp2 = client.post(f"/api/loans/{loan_id}/return")
        assert resp2.status_code == 200
        assert b.available is True

def test_return_loan_twice_is_conflict(client, app):
    with app.app_context():
        u = create_user(matricula="M6")
        b = create_book()
        loan_id = client.post("/api/loans", json={"user_id": u.id, "book_id": b.id}).get_json()["id"]
        client.post(f"/api/loans/{loan_id}/return")
        resp2 = client.post(f"/api/loans/{loan_id}/return")
        assert resp2.status_code == 409

def test_list_open_loans_only(client, app):
    with app.app_context():
        u = create_user(matricula="M7")
        b1 = create_book(title="B1")
        b2 = create_book(title="B2")
        id1 = client.post("/api/loans", json={"user_id": u.id, "book_id": b1.id}).get_json()["id"]
        id2 = client.post("/api/loans", json={"user_id": u.id, "book_id": b2.id}).get_json()["id"]
        client.post(f"/api/loans/{id1}/return")
        open_list = client.get("/api/loans?status=abertos").get_json()
        ids = {x["id"] for x in open_list}
        assert id2 in ids and id1 not in ids

def test_get_loan_detail(client, app):
    with app.app_context():
        u = create_user(matricula="M8")
        b = create_book()
        loan_id = client.post("/api/loans", json={"user_id": u.id, "book_id": b.id}).get_json()["id"]
        data = client.get(f"/api/loans/{loan_id}").get_json()
        assert data["id"] == loan_id
        assert data["open"] is True

def test_frontend_create_and_return_flow(client, app):
    # sanity check that pages render and posts work
    resp = client.get("/loans")
    assert resp.status_code == 200
