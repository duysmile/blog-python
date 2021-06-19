from flask import Blueprint, request, jsonify, make_response
import logging

from app.modules.like.model.like import LikeSchema
from ..biz.like_post import like_post, unlike_post
from ....middlewares.authenticate import token_required, user_required_info

like_post_api = Blueprint("like_posts", __name__)

@like_post_api.route("/posts/<post_id>/like", methods=["POST"])
@token_required
@user_required_info
def like_post_controller(current_user, post_id):
    try:
        data = LikeSchema().load({"post_id": post_id, "user_id": current_user.id})

        like_post(data)
        return make_response(jsonify({"data": True}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": str(e)}), 500)

@like_post_api.route("/posts/<post_id>/unlike", methods=["DELETE"])
@token_required
@user_required_info
def unlike_post_controller(current_user, post_id):
    try:
        data = LikeSchema().load({"post_id": post_id, "user_id": current_user.id})

        unlike_post(data)
        return make_response(jsonify({"data": True}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": str(e)}), 500)
