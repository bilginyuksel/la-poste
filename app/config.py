import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV_TYPE = "development"

    LETTER_TRACKING_CLIENT_BASE_URL = "https://api.laposte.fr/suivi/v2"
    LETTER_TRACKING_CLIENT_API_KEY = "2J7Gqn036YLsavqndlJHu+2/qO+ZikLeYmrScpCqpbzRe0Q7FAtkude3rz2N0WB0"


class TestingConfig(Config):
    ENV_TYPE = "testing"

    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    LETTER_TRACKING_CLIENT_BASE_URL = "https://api.laposte.fr/suivi/v2"
    LETTER_TRACKING_CLIENT_API_KEY = "2J7Gqn036YLsavqndlJHu+2/qO+ZikLeYmrScpCqpbzRe0Q7FAtkude3rz2N0WB0"


class ProductionConfig(Config):
    ENV_TYPE = "production"

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    LETTER_TRACKING_CLIENT_BASE_URL = os.getenv("LETTER_TRACKING_CLIENT_BASE_URL")
    LETTER_TRACKING_CLIENT_API_KEY = os.getenv("LETTER_TRACKING_CLIENT_API_KEY")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
