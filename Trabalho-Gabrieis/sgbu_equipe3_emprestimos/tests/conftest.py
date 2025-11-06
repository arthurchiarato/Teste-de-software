
import pytest
from app.app import create_app
from app.models import db

@pytest.fixture()
def app():
    app = create_app(testing=True)
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def _db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield
