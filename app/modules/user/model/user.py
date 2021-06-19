import re
from marshmallow import Schema, fields
from app import db

import enum

class Provider(enum.Enum):
    facebook = "facebook"
    google = "google"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.Enum(Provider))
    email = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def serialize(self):
        return {
            'id': self.id,
            'provider': self.provider,
            'email': self.email
        }

class FbInfo(db.Model):
    __tablename__ = "fb_informations"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    phone_number = db.Column(db.String(13))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(user_id, data):
        FbInfo.query.filter_by(user_id=user_id).update(data)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number
        }

class GgInfo(db.Model):
    __tablename__ = "gg_informations"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    occupation = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(user_id, data):
        GgInfo.query.filter_by(user_id=user_id).update(data)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }


class FbInfoSchema(Schema):
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True, validate=lambda x: re.match(r"(84|0[3|5|7|8|9])+([0-9]{8})", x))

class GgInfoSchema(Schema):
    name = fields.Str(required=True)
    occupation = fields.Str(required=True)