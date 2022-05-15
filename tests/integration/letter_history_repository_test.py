import pytest

from app.models.letter_history import LetterHistory
from app.repository import LetterHistoryRepository
from app import db, app, config


@pytest.fixture
def letter_history_repository():
    return LetterHistoryRepository(db)


@pytest.fixture(autouse=True)
def prepare_letter_repository_testing_data():
    app.config.from_object(config['testing'])

    db.create_all()

    yield

    db.drop_all()


def test_letter_history_insert(letter_history_repository):
    letter_history_repository.insert(
        LetterHistory(letter_id=5, status="Delivered"))

    history = LetterHistory.query.get(1)

    assert history.id == 1
    assert history.letter_id == 5
    assert history.status == "Delivered"


def test_letter_history_find_all(letter_history_repository):
    db.session.add(LetterHistory(letter_id=5, status="Delivered"))
    db.session.add(LetterHistory(letter_id=5, status="In Transit"))
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

    histories = letter_history_repository.find_all(5)

    assert len(histories) == 2
    assert histories[0].status == "Delivered"
    assert histories[1].status == "In Transit"
