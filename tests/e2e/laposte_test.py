import pytest
import time

from app import app, db
from app.config import config
from app.models.letter import Letter


@pytest.fixture(autouse=True)
def prepare_testing_environment():
    app.config.from_object(config["testing"])
    app.config.update({"TESTING": True})

    db.create_all()

    yield

    db.drop_all()


@pytest.fixture
def client():
    return app.test_client()


def test_fetch_letter(client):
    add_sample_letter_with_none_status("6A21757464334")

    res = client.get("/letters/1")

    assert res.status_code == 200
    assert res.json == {
        "id": 1,
        "tracking_number": "6A21757464334",
        "status": "Your parcel has been delivered"
    }


def test_update_all(client):
    add_sample_letter_with_none_status("6A21757464334")
    add_sample_letter_with_none_status("6A22658410765")

    res = client.put("/letters")

    assert res.status_code == 202

    time.sleep(2)

    first_letter = Letter.query.get(1)
    second_letter = Letter.query.get(2)

    assert first_letter.status == "Your parcel has been delivered"
    assert second_letter.status == "Your parcel has been delivered"


def add_sample_letter_with_none_status(tracking_number="6A21757464334"):
    db.session.add(Letter(tracking_number=tracking_number))
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
