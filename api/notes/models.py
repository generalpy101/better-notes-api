from api.server import db
from db.base_model_mixin import Base
from db.searchable_mixin import SearchableMixin


class Notes(Base, SearchableMixin):
    __tablename__ = "notes"
    __searchable__ = ["title", "content"]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

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
