import pytest
import os

from api.server import create_app
from api.server import db
from db.base_model_mixin import Base
from config import TestingConfig

from .utils import generate_random_note, seed_database, TEST_USER


# Create fixture for client
@pytest.fixture
def client():
    flask_app = create_app(TestingConfig)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            from api.auth.models import Users
            from api.notes.models import Notes

            Base.metadata.drop_all(bind=db.engine)
            Base.metadata.create_all(bind=db.engine)

            # Seed the database with a test user
            seed_database(db, Users, [TEST_USER])

            # Seed the database with some notes
            seed_database(db, Notes, [generate_random_note() for _ in range(10)])

            yield testing_client

            # Clean up after tests
            db.session.remove()
            Base.metadata.drop_all(bind=db.engine)

            # Delete the test database
            os.remove(TestingConfig.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", ""))


# Fixture for user jwt token
@pytest.fixture
def user_token(client):
    # Login the user
    response = client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "test",
        },
    )
    return response.json.get("token")
