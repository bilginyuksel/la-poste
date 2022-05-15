import pytest

from app.repository import LetterRepository
from app.models.letter import Letter
from app import app, db, config

@pytest.fixture
def letter_repository():
    return LetterRepository(db)


@pytest.fixture(autouse=True)
def prepare_letter_repository_testing_data():
    app.config.from_object(config['testing'])

    db.create_all()

    l = Letter(id=5, tracking_number="123456789", status="Delivered")
    try:
        db.session.add(l)
        db.session.commit()
    except Exception:
        db.session.rollback()

    yield

    db.drop_all()


def test_letter_repository_get(letter_repository):
    letter = letter_repository.get(5)

    assert letter.id == 5
    assert letter.tracking_number == "123456789"
    assert letter.status == "Delivered"


def test_letter_repository_update(letter_repository):
    letter_repository.update(5, status="In Transit")

    assert Letter.query.get(5).status == "In Transit"
