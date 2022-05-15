from app import db


class LetterHistory(db.Model):
    __tablename__ = "letter_histories"

    id = db.Column(db.Integer, primary_key=True)
    letter_id = db.Column(db.Integer, db.ForeignKey("letter.id"))
    status = db.Column(db.String(191))
