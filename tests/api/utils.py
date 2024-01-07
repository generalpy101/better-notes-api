import random
import string

from werkzeug.security import generate_password_hash

TEST_USER = {
    "username": "test",
    "password": generate_password_hash("test"),
}


def generate_random_string(length=10):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_random_note():
    return {
        "title": generate_random_string(),
        "content": generate_random_string(20),
        "user_id": 1,
    }


def seed_database(db, model, data):
    for item in data:
        db.session.add(model(**item))
    db.session.commit()
