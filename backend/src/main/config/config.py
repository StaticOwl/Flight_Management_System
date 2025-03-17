import os
import defaults


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", defaults.DATABASE_URL)

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "stage": StagingConfig,
    "prod": ProductionConfig
}
