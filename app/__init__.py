from .client import *
from . import models
from .views import *
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.config import config

app = Flask(__name__)

CORS(app, origins="*", supports_credentials=True)

config_name = os.getenv("FLASK_CONFIG") or "default"
app.config.from_object(config[config_name])

db = SQLAlchemy(app)


def create_letter_service():
    from . import service
    from . import repository

    conf = config[config_name]

    return service.LetterService(
        repository.LetterRepository(db),
        repository.LetterHistoryRepository(db),
        client.LetterTrackingClient(
            conf.LETTER_TRACKING_CLIENT_BASE_URL,
            conf.LETTER_TRACKING_CLIENT_API_KEY
        )
    )


__letter_service = create_letter_service()

letter_view = LetterView(__letter_service)
letter_view.register_routes(app)
