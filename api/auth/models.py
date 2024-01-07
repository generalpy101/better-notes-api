from werkzeug.security import generate_password_hash, check_password_hash
from api.server import db
from db.base_model_mixin import Base


class Users(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    password = db.Column(db.String(256))

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def upsert(cls, new_model_object, old_model_object=None):
        # Hash the password before saving to database
        new_model_object.password = generate_password_hash(new_model_object.password)
        return super().upsert(new_model_object, old_model_object)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User: Username - {}; password - {};>".format(self.username, self.pwd)


class InvalidToken(Base):
    __tablename__ = "invalid_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)

    @classmethod
    def is_invalid(cls, jti):
        """Determine whether the jti key is on the blocklist return bool"""
        query = cls.filter(cls.jti == jti).first()
        return bool(query)
