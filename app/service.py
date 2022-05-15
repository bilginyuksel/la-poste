from .models.letter_history import LetterHistory


class LetterNotFoundException(Exception):
    pass


class LetterService:
    def __init__(self, letter_repository, letter_history_repository, letter_tracking_client):
        self.__repository = letter_repository
        self.__history_repository = letter_history_repository
        self.__tracking_client = letter_tracking_client

    def fetch(self, id):
        letter = self.__repository.get(id)
        if letter is None:
            raise LetterNotFoundException

        timelines = sorted(self.__tracking_client.get_letter_tracking_history(
            letter.tracking_number),
            key=lambda x: x.id
        )

        if not timelines:
            return letter

        last_timeline = timelines[-1]
        if last_timeline.status == letter.status:
            return letter

        self.__create_history_records(letter, timelines)
        self.__repository.update(letter.id, status=last_timeline.status)

        letter.status = last_timeline.status
        return letter

    def __create_history_records(self, letter, timelines):
        current_timeline_index = 0
        for idx, timeline in enumerate(timelines):
            if timeline.status == letter.status:
                current_timeline_index = idx
                break

        for timeline in timelines[current_timeline_index:]:
            self.__history_repository.insert(LetterHistory(
                letter_id=letter.id,
                status=timeline.status
            ))

    def update_all(self):
        letters = self.__repository.find_all()

        for letter in letters:
            self.fetch(letter.id)
