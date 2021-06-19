import re
from marshmallow import Schema, fields
from dataclasses import dataclass

from app import db

import enum

@dataclass
class Post(db.Model):
    id: int
    title: str
    summary: str
    content: str

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(1000))
    summary = db.Column(db.String(2000))
    content = db.Column(db.Text())

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(id, data):
        Post.query.filter_by(id=id).update(data)
        db.session.commit()

class PostSchema(Schema):
    title = fields.Str(required=True, validate=lambda x: len(x) <= 1000)
    summary = fields.Str(required=True, validate=lambda x: len(x) <= 2000)
    content = fields.Str(required=True)