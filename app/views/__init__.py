from abc import ABC, abstractmethod
import threading

STATUS_ACCEPTED = 202


class View(ABC):
    @abstractmethod
    def register_routes(self, app):
        raise NotImplementedError


# Error handler could be added to handle error cases
class LetterView(View):
    def __init__(self, letter_service):
        self.__letter_service = letter_service

        self.__update_all_thread = threading.Thread(
            target=self.__letter_service.update_all)
        self.__update_all_thread_lock = threading.Lock()

    def register_routes(self, app):
        app.add_url_rule("/letters/<int:id>", "fetch",
                         view_func=self.fetch, methods=["GET"])
        app.add_url_rule("/letters", "update_all",
                         view_func=self.update_all, methods=["PUT"])

    def fetch(self, id):
        letter = self.__letter_service.fetch(id)
        return {
            "id": letter.id,
            "tracking_number": letter.tracking_number,
            "status": letter.status
        }

    def update_all(self):
        """
        Update all updates all letters in the database asyncronously
        It immediately returns a 202 status code
        Then starts the update_all thread

        To not create a new thread for every request,
        we use a lock to ensure only one thread is running at a time
        """
        self.__update_all_thread_lock.acquire()
        if not self.__update_all_thread.is_alive():
            self.__update_all_thread = threading.Thread(
                target=self.__letter_service.update_all)
            self.__update_all_thread.start()
        self.__update_all_thread_lock.release()

        return ('', STATUS_ACCEPTED)
