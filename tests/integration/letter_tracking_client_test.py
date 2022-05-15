
import pytest

from app import LetterTrackingClient, Timeline
from app.config import TestingConfig


@pytest.fixture
def letter_tracking_client():
    return LetterTrackingClient(
        base_url=TestingConfig.LETTER_TRACKING_CLIENT_BASE_URL,
        api_key=TestingConfig.LETTER_TRACKING_CLIENT_API_KEY
    )


def test_get_letter_tracking_history_timeline_exists(letter_tracking_client):
    timelines = letter_tracking_client.get_letter_tracking_history(
        "6A21757464334")

    expected_timelines = [
        Timeline(1, "Your parcel is now being processed by La Poste."),
        Timeline(2, "It is being processed in our network."),
        Timeline(3, "Your parcel has arrived at its delivery site."),
        Timeline(4, "We are preparing your parcel for delivery."),
        Timeline(5, "Your parcel has been delivered"),
    ]

    for expected_timeline, timeline in zip(expected_timelines, sorted(timelines, key=lambda x: x.id)):
        assert expected_timeline.id == timeline.id
        assert expected_timeline.status == timeline.status


def test_get_letter_tracking_history_wrong_tracking_number(letter_tracking_client):
    with pytest.raises(Exception):
        letter_tracking_client.get_letter_tracking_history("WR0N5_NUM8ER")


def test_get_letter_tracking_history_timeline_does_not_exist(letter_tracking_client):
    timelines = letter_tracking_client.get_letter_tracking_history(
        "3C00638718711")

    assert timelines == []
