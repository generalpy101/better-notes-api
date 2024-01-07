from api.server import jwt
from api.auth import auth_bp
from api.auth.helpers import *
from api.auth.models import InvalidToken
from api.auth.schema import UserSchema
from core.views.response import APIDataResponse, APIErrorResponse, APIMessageResponse
from core.errors.api_errors import InvalidCredentialsError, InvalidUsageError
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@jwt.token_in_blocklist_loader
def check_if_blacklisted_token(data, decrypted):
    """
    Decorator designed to check for blacklisted tokens
    """
    jti = decrypted["jti"]
    return InvalidToken.is_invalid(jti)


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user_schema_object = user_schema.load(data)

        user = get_user_using_credentials(user_schema_object)
        if user is not None:
            token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify({"token": token, "refreshToken": refresh_token})
        else:
            raise InvalidCredentialsError(
                error_message="Invalid Credentials",
                description="Username or password is incorrect",
            )
    except InvalidCredentialsError as e:
        return APIErrorResponse(
            error=e.error_message,
            description=e.description,
            error_type="InvalidCredentials",
            status_code=401,
        )
    except Exception as e:
        return APIErrorResponse(
            error="Internal Server Error",
            description=str(e),
            error_type="InternalServerError",
            status_code=500,
        )


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        user = user_schema.load(data)

        if check_if_username_is_taken(user.get("username")):
            raise InvalidUsageError(
                error_message="Username is taken",
                description=f"Username {user.get('username')} is already taken",
            )

        user = add_user(user)
        return APIDataResponse(data=user_schema.dump(user), status_code=201)
    except InvalidUsageError as e:
        return APIErrorResponse(
            error=e.error_message,
            description=e.description,
            error_type="InvalidUsage",
            status_code=400,
        )
    except Exception as e:
        return APIErrorResponse(
            error="Internal Server Error",
            description=str(e),
            error_type="InternalServerError",
            status_code=500,
        )


@auth_bp.route("/logout/refresh", methods=["POST"])
@jwt_required()
def logout():
    """
    End-point to invalidate the token.
    Can be used with both log the user out or for the frontend to call after refreshing the token.
    """
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return APIMessageResponse(message="Successfully logged out", status_code=200)
    except Exception as e:
        return APIErrorResponse(
            error="Internal Server Error",
            description=str(e),
            error_type="InternalServerError",
            status_code=500,
        )


@auth_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_account():
    try:
        user = get_user(get_jwt_identity())
        remove_user(user.id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})
