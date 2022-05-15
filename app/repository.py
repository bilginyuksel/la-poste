from .models.letter_history import LetterHistory
from .models.letter import Letter


class LetterRepository:
    def __init__(self, db):
        self.db = db

    def get(self, id):
        return Letter.query.get(id)

    def update(self, letter_id, status=None):
        args = {}
        if status:
            args["status"] = status

        Letter.query.filter(Letter.id == letter_id).update(args)

        try:
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()

    def find_all(self):
        return Letter.query.all()


class LetterHistoryRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, history: LetterHistory):
        self.db.session.add(history)

        try:
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()

    def find_all(self, letter_id):
        return LetterHistory.query.filter(LetterHistory.letter_id == letter_id).all()
