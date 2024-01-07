from api.server import ma
from api.notes.models import Notes


class NotesCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Notes

    title = ma.String(required=True)
    content = ma.String(required=True)

    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)

    user_id = ma.Integer(dump_only=True)


class NotesUpdateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Notes

    title = ma.String(required=False)
    content = ma.String(required=False)

    created_at = ma.DateTime(dump_only=True)
    updated_at = ma.DateTime(dump_only=True)

    user_id = ma.Integer(dump_only=True)
