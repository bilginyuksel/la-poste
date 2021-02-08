from app import app
from app.models.letter import Letter


@app.route("/ping", methods=["GET"])
def ep_ping():
    return "pong", 200


@app.route("/letters", methods=["POST"])
def ep_setup_create_letter():
    # Example of ORM usage (SQLAlchemy)
    letter = Letter()
    db.session.add(letter)
    db.session.commit()
    return f"All done: letter object {letter.id} has been created", 200
