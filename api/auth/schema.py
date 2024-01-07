from api.auth.models import Users
from api.server import ma
from werkzeug.security import generate_password_hash


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users

    username = ma.String(required=True)
    password = ma.String(required=True, load_only=True)
    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)
    id = ma.Integer(dump_only=True)
