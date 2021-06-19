from flask import Blueprint, request, jsonify, make_response
import logging

from ..biz.get_post import get_post
from ..model.post import PostDetailSchema

get_post_api = Blueprint("get_post", __name__)

@get_post_api.route("/<post_id>", methods=["GET"])
def get_post_controller(post_id):
    try:
        post_id = int(post_id)
        if post_id < 0:
            return make_response(jsonify({
                "error": "invalid post id",
            }), 400)

        post = get_post(post_id)

        return make_response(jsonify({
            "data": PostDetailSchema().load(post),
        }), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": str(e)}), 500)
