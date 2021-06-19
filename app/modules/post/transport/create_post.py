from flask import Blueprint, request, jsonify, make_response
import flask
import logging

from app.modules.post.model.post import PostSchema
from ..biz.create_post import create_post_biz
from ....middlewares.authenticate import token_required, user_required_info

create_post_api = Blueprint("/posts", __name__)

@create_post_api.route("", methods=["POST"])
@token_required
# @user_required_info
def create_post(current_user):
    try:
        data = request.get_json()
        data = PostSchema().load(data)

        create_post_biz(current_user.id, data)
        return make_response(jsonify({"data": True}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": "cannot create post"}), 500)
