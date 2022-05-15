import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV_TYPE = "development"


class TestingConfig(Config):
    ENV_TYPE = "testing"

    SQLALCHEMY_DATABASE_URI = "sqlite:///e2e_testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    LETTER_TRACKING_CLIENT_BASE_URL = "https://api.laposte.fr/suivi/v2"
    LETTER_TRACKING_CLIENT_API_KEY = "2J7Gqn036YLsavqndlJHu+2/qO+ZikLeYmrScpCqpbzRe0Q7FAtkude3rz2N0WB0"


class ProductionConfig(Config):
    ENV_TYPE = "production"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
