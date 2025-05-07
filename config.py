import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a_very_secret_key_that_should_be_changed"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///../sandbox_db/devskillforge.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

