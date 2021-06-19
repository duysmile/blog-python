from flask import Blueprint, request, jsonify, make_response
import logging
from datetime import datetime

from ..model.like import ListLikeSchema
from ..biz.list_like import list_all_like_by_post

list_like_by_post_api = Blueprint("list_likes_by_post", __name__)

@list_like_by_post_api.route("/posts/<post_id>/likes", methods=["GET"])
def list_like_controller(post_id):
    try:
        cursor = request.args.get('cursor')
        if cursor is not None:
            cursor = int(cursor)

        names, likes = list_all_like_by_post(post_id, cursor)

        for i in range(len(names)):
            names[i] = ListLikeSchema().load({"user_name": names[i]})

        if len(likes) > 0:
            next_cursor = datetime.timestamp(likes[-1].created_on)
            next_cursor = str(int(next_cursor))
        else:
            next_cursor = ""

        return make_response(jsonify({
            "data": names,
            "next_cursor": next_cursor,
        }), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": str(e)}), 500)
