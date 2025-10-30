
from __future__ import annotations
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from .models import db, User, Book, Loan
from .seed import seed_example_data

def create_app(testing: bool = False):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sgbu.db" if not testing else "sqlite://"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev"
    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_example_data()

    # ---------- Frontend pages ----------
    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/loans")
    def loans_page():
        status = request.args.get("status", "abertos")
        q = Loan.query
        if status == "abertos":
            q = q.filter(Loan.return_date.is_(None))
        loans = q.order_by(Loan.id.desc()).all()
        users = User.query.order_by(User.name).all()
        books = Book.query.filter_by(available=True).order_by(Book.title).all()
        return render_template("loans.html", loans=loans, users=users, books=books, status=status)

    @app.post("/loans/new")
    def loans_new():
        user_id = request.form.get("user_id", type=int)
        book_id = request.form.get("book_id", type=int)
        loan_days = request.form.get("loan_days", default=7, type=int)

        user = User.query.get(user_id)
        book = Book.query.get(book_id)
        if not user:
            flash("Usuário inválido.", "danger")
            return redirect(url_for("loans_page"))
        if not book:
            flash("Livro inválido.", "danger")
            return redirect(url_for("loans_page"))
        if not book.available:
            flash("Livro indisponível.", "warning")
            return redirect(url_for("loans_page"))

        loan = Loan(user_id=user.id, book_id=book.id, due_date=Loan.make_due_date(loan_days))
        book.available = False
        db.session.add(loan)
        db.session.commit()
        flash("Empréstimo criado com sucesso!", "success")
        return redirect(url_for("loans_page"))

    @app.post("/loans/<int:loan_id>/return")
    def loans_return(loan_id: int):
        loan = Loan.query.get_or_404(loan_id)
        try:
            loan.register_return()
            db.session.commit()
            flash("Devolução registrada.", "success")
        except ValueError as e:
            flash(str(e), "warning")
        return redirect(url_for("loans_page"))

    # ---------- REST API ----------
    @app.get("/api/loans")
    def api_loans():
        status = request.args.get("status", "abertos")
        q = Loan.query
        if status == "abertos":
            q = q.filter(Loan.return_date.is_(None))
        loans = q.order_by(Loan.id.desc()).all()
        return jsonify([{
            "id": l.id,
            "user": {"id": l.user.id, "name": l.user.name},
            "book": {"id": l.book.id, "title": l.book.title},
            "loan_date": l.loan_date.isoformat(),
            "due_date": l.due_date.isoformat(),
            "return_date": l.return_date.isoformat() if l.return_date else None,
        } for l in loans])

    @app.get("/api/loans/<int:loan_id>")
    def api_loan_detail(loan_id: int):
        l = Loan.query.get_or_404(loan_id)
        return jsonify({
            "id": l.id,
            "user_id": l.user_id,
            "book_id": l.book_id,
            "loan_date": l.loan_date.isoformat(),
            "due_date": l.due_date.isoformat(),
            "return_date": l.return_date.isoformat() if l.return_date else None,
            "open": l.return_date is None
        })

    @app.post("/api/loans")
    def api_create_loan():
        data = request.get_json(silent=True) or {}
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        loan_days = int(data.get("loan_days", 7))

        user = User.query.get(user_id)
        book = Book.query.get(book_id)
        if not user:
            return jsonify({"error": "Usuário inexistente"}), 400
        if not book:
            return jsonify({"error": "Livro inexistente"}), 400
        if not book.available:
            return jsonify({"error": "Livro indisponível"}), 409

        loan = Loan(user_id=user.id, book_id=book.id, due_date=Loan.make_due_date(loan_days))
        book.available = False
        db.session.add(loan)
        db.session.commit()
        return jsonify({"id": loan.id}), 201

    @app.post("/api/loans/<int:loan_id>/return")
    def api_return_loan(loan_id: int):
        loan = Loan.query.get_or_404(loan_id)
        try:
            loan.register_return()
            db.session.commit()
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        return jsonify({"ok": True})

    return app

# for flask run
app = create_app()
