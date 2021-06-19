import re
from marshmallow import Schema, fields
from dataclasses import dataclass

from app import db

import enum

@dataclass
class Like(db.Model):
    user_id: int
    post_id: int

    __tablename__ = "post_likes"
    user_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, primary_key=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(id, data):
        Post.query.filter_by(id=id).update(data)
        db.session.commit()

class LikeSchema(Schema):
    post_id = fields.Int(required=True, validate=lambda x: 0 < x)
    user_id = fields.Int(required=True, validate=lambda x: 0 < x)