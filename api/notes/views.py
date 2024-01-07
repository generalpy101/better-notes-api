from flask import jsonify, request

from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

from api.server import db

from api.auth.models import Users
from api.notes.models import Notes
from api.notes.schema import NotesCreateSchema, NotesUpdateSchema
from api.notes import notes_bp
from core.views.base_view import BaseView
from core.views.response import APIListResponse

note_schema = NotesCreateSchema()
notes_schema = NotesCreateSchema(many=True)


class NotesView(BaseView):
    post_schema = NotesCreateSchema()
    put_schema = NotesUpdateSchema()
    model = Notes

    # @jwt_required()
    # def get(self, id=None):
    #     try:
    #         current_user = get_jwt_identity()
    #         if id:
    #             # Get note by id and user_id or if the note is shared with the user
    #             obj = self.model.filter(
    #                 self.model.id == id,
    #                 or_(
    #                     self.model.user_id == current_user,
    #                     self.model.shared_users.any(Users.id == current_user)
    #                 )
    #             )
    #             if not obj:
    #                 return self.get_message_response(404, "Object not found")
    #             return self.get_data_response(self.schema.dump(obj), 200)
    #         else:
    #             return super().get(id)
    #     except Exception as e:
    #         return self.handle_error(e)


notes_view = NotesView.as_view("notes_view")
notes_bp.add_url_rule(
    "/",
    view_func=notes_view,
    methods=["GET"],
    defaults={"id": None},
    strict_slashes=False,
)
notes_bp.add_url_rule("/", view_func=notes_view, methods=["POST"], strict_slashes=False)
notes_bp.add_url_rule(
    "/<int:id>",
    view_func=notes_view,
    methods=["GET", "PUT", "DELETE"],
    strict_slashes=False,
)


@notes_bp.route("/search", methods=["GET"])
@jwt_required()
def search_notes():
    q = request.args.get("q")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    notes, total = Notes.search(q, page, per_page)

    notes = notes_schema.dump(notes)
    return APIListResponse(data=notes, status_code=200, count=total)


# @notes_bp.route('/<int:note_id>/share', methods=['POST'])
# @jwt_required()
# def share_note_with_users(note_id):
#     current_user_id = get_jwt_identity()

#     note = Notes.filter(Notes.id==note_id, Notes.user_id == current_user_id).first()
#     if not note:
#         return jsonify({"message": "Note not found or unauthorized"}), 404

#     # Get the list of user IDs to share the note with from the request JSON
#     users_to_share_ids = request.json.get('users_ids', [])  # Assuming 'users_ids' is passed as a list in JSON

#     # Retrieve users from the IDs
#     users_to_share_with = Users.filter(Users.id.in_(users_to_share_ids)).all()

#     # Share the note with multiple users
#     for user in users_to_share_with:
#         note.shared_with.append(user)

#     db.session.commit()

#     return jsonify({"message": "Note shared successfully"}), 200
