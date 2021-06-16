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

