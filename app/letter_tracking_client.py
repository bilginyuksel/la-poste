import requests


class Timeline:
    def __init__(self, id, short_label):
        self.id = id
        self.status = short_label
    


class LetterTrackingClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

        self.default_headers = {
            "X-Okapi-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.default_params = {"lang": "en_GB"}

    def get_letter_tracking_history(self, tracking_number):
        """
        Send a request to the API to get the shipment timelines for the given tracking number.
        If returnCode is 104 (no tracking information is available right now), so it returns an empty list.
        If returnCode is 200 (OK), it returns a list of Timeline objects.

        Otherwise it raises an Exception.
        """
        response = requests.get(
            f"{self.base_url}/idships/{tracking_number}",
            headers=self.default_headers,
            params=self.default_params
        )
        body = response.json()

        if body["returnCode"] == 104:
            return []
        elif body["returnCode"] == 200:
            return [
                Timeline(timeline["id"], timeline["shortLabel"])
                for timeline in body["shipment"]["timeline"]
            ]

        raise Exception(f"Unknown error returned by tracking api, {body}")
