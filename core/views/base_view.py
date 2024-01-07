from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from core.errors.api_errors import ValidationError, NotFoundError
from core.views.response import APIDataResponse, APIListResponse
from db.base_model_mixin import BaseModelMixin


class BaseView(MethodView):
    post_schema = None  # Marshmallow schema to be set in subclasses
    put_schema = None  # Marshmallow schema to be set in subclasses
    model: BaseModelMixin = None  # Model to be set in subclasses

    def __init__(self):
        super().__init__()
        if not self.post_schema or not self.model:
            raise NotImplementedError("Please set schema and model in subclasses")

    @jwt_required()
    def get(self, id=None):
        try:
            current_user = get_jwt_identity()
            if id:
                if hasattr(self.model, "user_id"):
                    obj = self.model.filter(
                        self.model.id == id, self.model.user_id == current_user
                    ).first()
                else:
                    obj = self.model.get_by_id(id)
                if not obj:
                    raise NotFoundError(
                        "Object not found",
                        f"{self.model.__name__} with id {id} not found",
                    )
                return APIDataResponse(data=self.post_schema.dump(obj), status_code=200)
            else:
                objects = self.model.filter().all()
                objects_dump = self.post_schema.dump(objects, many=True)
                return APIListResponse(
                    data=objects_dump, status_code=200, count=len(objects_dump)
                )
        except Exception as e:
            raise e

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            validated_data = self.post_schema.load(data)
            new_obj = self.model(**validated_data)
            if hasattr(new_obj, "user_id"):
                new_obj.user_id = get_jwt_identity()
            new_obj = self.model.upsert(new_model_object=new_obj)
            return APIDataResponse(data=self.post_schema.dump(new_obj), status_code=201)
        except Exception as e:
            if isinstance(e, MarshmallowValidationError):
                raise ValidationError(
                    error_message="Schema validation error", description=str(e.messages)
                )
            else:
                raise e

    @jwt_required()
    def put(self, id):
        try:
            # If put schema is not set, use post schema
            if not self.put_schema:
                self.put_schema = self.post_schema
            data = request.get_json()
            if hasattr(self.model, "user_id"):
                obj = self.model.filter(
                    self.model.id == id, self.model.user_id == get_jwt_identity()
                ).first()
            else:
                obj = self.model.get_by_id(id)
            if not obj:
                raise NotFoundError(
                    "Object not found", f"{self.model.__name__} with id {id} not found"
                )
            validated_data = self.put_schema.load(data)
            new_obj = self.model(**validated_data)
            new_obj.id = id
            if hasattr(new_obj, "user_id"):
                new_obj.user_id = get_jwt_identity()
            new_obj = self.model.upsert(new_model_object=new_obj, old_model_object=obj)
            return APIDataResponse(data=self.put_schema.dump(new_obj), status_code=200)
        except Exception as e:
            if isinstance(e, MarshmallowValidationError):
                raise ValidationError(
                    error_message="Schema validation error", description=str(e.messages)
                )
            else:
                raise e

    @jwt_required()
    def delete(self, id):
        try:
            current_user = get_jwt_identity()
            # Get current user's object if user_id is present in model
            if hasattr(self.model, "user_id"):
                obj = self.model.filter(
                    self.model.id == id, self.model.user_id == current_user
                ).first()
            else:
                obj = self.model.get_by_id(id)
            if not obj:
                raise NotFoundError(
                    "Object not found", f"{self.model.__name__} with id {id} not found"
                )

            obj.delete(id=id)
            return APIDataResponse(data=self.post_schema.dump(obj), status_code=200)
        except Exception as e:
            raise e
