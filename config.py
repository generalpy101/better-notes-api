import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-super-secret"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
    ELASTICSEARCH_USERNAME = os.environ.get("ELASTICSEARCH_USERNAME") or "elastic"
    ELASTICSEARCH_PASSWORD = os.environ.get("ELASTICSEARCH_PASSWORD") or "elastic"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")