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


class ProductionConfig(Config):
    ENV_TYPE = "production"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
