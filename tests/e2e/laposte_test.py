from app.config import config
import pytest
from app import app, db
from app.models.letter import Letter


@pytest.fixture(autouse=True)
def prepare_testing_environment():
    app.config.from_object(config["testing"])
    app.config.update({"TESTING": True})

    db.create_all()

    db.session.add(Letter(tracking_number="6A21757464334"))
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture
def client():
    return app.test_client()


def test_fetch_letter(client):
    res = client.get("/letters/1")

    assert res.status_code == 200
    assert res.json == {
        "id": 1,
        "tracking_number": "6A21757464334",
        "status": "Your parcel has been delivered"
    }
