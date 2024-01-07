from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base
from api.server import db


class BaseModelMixin:
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __prepare_for_upsert(self):
        """Prepare the model for upsertion"""
        self.updated_at = db.func.now()

    def __prepare_for_insert(self):
        """Prepare the model for insertion"""
        self.created_at = db.func.now()

    def to_dict(self):
        """Return a dictionary representation of the model"""
        data_dict = {}

        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            data_dict[key] = value

        return data_dict

    def update(self, **kwargs):
        """Update the model object"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def upsert(cls, new_model_object, old_model_object=None):
        """Update or insert a model object"""
        new_model_object.__prepare_for_upsert()

        if old_model_object is None:
            # This is insert case
            new_model_object.__prepare_for_insert()

            db.session.add(new_model_object)
            db.session.commit()
        else:
            # This is update case
            old_model_object.update(**new_model_object.to_dict())

            db.session.flush([old_model_object])
            db.session.commit()

        return cls.get_by_id(new_model_object.id)

    @classmethod
    def get_by_id(cls, id):
        """Return a model object by id"""
        return cls.filter(cls.id == id).first()

    @classmethod
    def get_all(cls):
        """Return all model objects"""
        return cls.filter().all()

    @classmethod
    def delete(cls, id):
        """Delete a model object"""
        db.session.query(cls).filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def filter(cls, *criterion):
        query_obj = db.session.query(cls)
        return query_obj.filter(*criterion)


Base = declarative_base(cls=BaseModelMixin)
metadata = Base.metadata
