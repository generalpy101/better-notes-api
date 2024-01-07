from api.server import db
from db.base_model_mixin import Base
from db.searchable_mixin import SearchableMixin
from api.auth.models import Users

# shared_notes = db.Table(
#     'shared_notes',
#     db.Column('note_id', db.Integer, db.ForeignKey('public.notes.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('public.users.id')),
#     schema='public'
# )


class Notes(Base, SearchableMixin):
    __tablename__ = "notes"
    __searchable__ = ["title", "content"]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # shared_users = db.relationship(
    #     'Users',
    #     secondary=shared_notes,
    #     primaryjoin=(id == shared_notes.c.note_id),
    #     secondaryjoin=(user_id == shared_notes.c.user_id),
    #     backref=db.backref('shared_notes', lazy='dynamic'),
    #     lazy='dynamic'
    # )
    @classmethod
    def upsert(cls, new_model_object, old_model_object=None):
        return super().upsert(new_model_object, old_model_object)

    def __init__(self, title=None, content=None, user_id=None, id=None):
        self.title = title
        self.content = content
        self.id = id
        self.user_id = user_id

    def __repr__(self):
        return "<Note: Title - {}; Content - {}; User ID - {};>".format(
            self.title, self.content, self.user_id
        )
