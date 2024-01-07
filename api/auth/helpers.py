from api.server import db
from api.auth.models import Users
from werkzeug.security import check_password_hash


def check_if_username_is_taken(username):
    return Users.filter(Users.username == username).first() != None


def get_users():
    users = Users.get_all()
    return [{"id": i.id, "username": i.username, "pwd": i.pwd} for i in users]


def get_user(user_id):
    users = Users.get_all()
    user = list(filter(lambda x: x.id == user_id, users))[0]
    return {"id": user.id, "username": user.username, "pwd": user.pwd}


def add_user(user_schema_object):
    if user_schema_object:
        user = Users(**user_schema_object)
        return Users.upsert(new_model_object=user)
    else:
        return {}


def remove_user(user_id):
    if user_id:
        try:
            user = Users.get_by_id(user_id)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


def get_user_using_credentials(user_schema_object):
    user = Users.filter(
        Users.username == user_schema_object.get("username"),
    ).first()
    if user is not None:
        if user.validate_password(user_schema_object.get("password")):
            return user
    return None
