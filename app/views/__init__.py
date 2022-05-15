from abc import ABC, abstractmethod


class View(ABC):
    @abstractmethod
    def register_routes(self, app):
        raise NotImplementedError


class LetterView(View):
    def register_routes(self, app):
        app.add_url_rule("/letters/<int:id>", "fetch", view_func=self.fetch)

    def fetch(self, id):
        return {
            "id": id,
            "tracking_number": "6A21757464334",
            "status": "Your parcel has been delivered"
        }
