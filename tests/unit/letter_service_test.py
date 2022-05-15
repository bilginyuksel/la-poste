import pytest

from app.client import LetterTrackingClient, Timeline
from app.models.letter import Letter
from app.repository import LetterHistoryRepository, LetterRepository

from app.service import LetterNotFoundException, LetterService


class FakeLetterRepository(LetterRepository):
    def __init__(self):
        self.letters = []

    def get(self, id):
        if id > len(self.letters):
            return None

        return self.letters[id-1]

    def update(self, id, status):
        self.letters[id-1].status = status

    def find_all(self):
        return self.letters


class FakeLetterHistoryRepository(LetterHistoryRepository):
    def __init__(self):
        self.history = []

    def insert(self, history):
        self.history.append(history)


class FakeLetterTrackingClient(LetterTrackingClient):
    def __init__(self):
        pass

    def get_letter_tracking_history(self, tracking_number):
        if tracking_number == "22":
            # unordered sample timeline list
            return [
                Timeline(1, "Letter has been prepared"),
                Timeline(3, "Your parcel has been delivered"),
                Timeline(2, "Delivery started"),
            ]
        elif tracking_number == "44":
            return [
                Timeline(1, "Pending"),
                Timeline(2, "Delivered"),
            ]
        elif tracking_number == "55":
            return []
        elif tracking_number == "33":
            raise Exception


@pytest.fixture
def fake_letter_history_repository():
    return FakeLetterHistoryRepository()


@pytest.fixture
def fake_letter_repository():
    return FakeLetterRepository()


@pytest.fixture
def fake_letter_tracking_client():
    return FakeLetterTrackingClient()


@pytest.fixture
def letter_service(fake_letter_repository, fake_letter_history_repository, fake_letter_tracking_client):
    return LetterService(
        fake_letter_repository,
        fake_letter_history_repository,
        fake_letter_tracking_client
    )


def test_letter_service_fetch_letter_not_found(
        fake_letter_repository,
        fake_letter_history_repository,
        letter_service
):
    fake_letter_repository.letters = []
    fake_letter_history_repository.history = []

    with pytest.raises(LetterNotFoundException):
        letter_service.fetch(1)

    assert len(fake_letter_history_repository.history) == 0


def test_letter_service_fetch_no_tracking_data_empty_timeline(
        fake_letter_repository,
        fake_letter_history_repository,
        letter_service
):
    fake_letter_repository.letters = [
        Letter(id=1, tracking_number="55", status="Pending")]
    fake_letter_history_repository.history = []

    l = letter_service.fetch(1)

    assert l.id == 1
    assert l.tracking_number == "55"
    assert l.status == "Pending"

    assert len(fake_letter_history_repository.history) == 0

    assert fake_letter_repository.letters[0].status == "Pending"

def test_letter_service_fetch_same_status(
    fake_letter_repository,
    fake_letter_history_repository,
    letter_service
):
    fake_letter_repository.letters = [
        Letter(id=1, tracking_number="22", status="Your parcel has been delivered"),
    ]

    letter_service.fetch(1)

    assert len(fake_letter_history_repository.history) == 0
    assert fake_letter_repository.letters[0].status == "Your parcel has been delivered"


def test_letter_service_fetch(
        fake_letter_repository,
        fake_letter_history_repository,
        letter_service
):
    fake_letter_repository.letters = [
        Letter(id=1, tracking_number="22", status=None)]
    fake_letter_history_repository.history = []

    l = letter_service.fetch(1)

    assert l.id == 1
    assert l.tracking_number == "22"
    assert l.status == "Your parcel has been delivered"

    assert len(fake_letter_history_repository.history) == 3
    assert fake_letter_history_repository.history[0].letter_id == 1
    assert fake_letter_history_repository.history[0].status == "Letter has been prepared"
    assert fake_letter_history_repository.history[1].letter_id == 1
    assert fake_letter_history_repository.history[1].status == "Delivery started"
    assert fake_letter_history_repository.history[2].letter_id == 1
    assert fake_letter_history_repository.history[2].status == "Your parcel has been delivered"

    assert fake_letter_repository.letters[0].status == "Your parcel has been delivered"


def test_letter_service_update_all(
        fake_letter_repository,
        fake_letter_history_repository,
        letter_service
):
    fake_letter_repository.letters = [
        Letter(id=1, tracking_number="22", status=None),
        Letter(id=2, tracking_number="44", status=None),
        Letter(id=3, tracking_number="55", status=None)
    ]

    letter_service.update_all()

    assert len(fake_letter_history_repository.history) == 5
    assert fake_letter_history_repository.history[0].letter_id == 1
    assert fake_letter_history_repository.history[0].status == "Letter has been prepared"
    assert fake_letter_history_repository.history[1].letter_id == 1
    assert fake_letter_history_repository.history[1].status == "Delivery started"
    assert fake_letter_history_repository.history[2].letter_id == 1
    assert fake_letter_history_repository.history[2].status == "Your parcel has been delivered"
    assert fake_letter_history_repository.history[3].letter_id == 2
    assert fake_letter_history_repository.history[3].status == "Pending"
    assert fake_letter_history_repository.history[4].letter_id == 2
    assert fake_letter_history_repository.history[4].status == "Delivered"

    assert fake_letter_repository.letters[0].status == "Your parcel has been delivered"
    assert fake_letter_repository.letters[1].status == "Delivered"
    assert fake_letter_repository.letters[2].status == None
