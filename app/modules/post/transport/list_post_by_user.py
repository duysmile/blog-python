from flask import Blueprint, request, jsonify, make_response
import logging

from ..model.post import ListPostSchema
from ..biz.list_post import list_post_by_user

list_post_by_user_api = Blueprint("list_posts_by_user", __name__)

@list_post_by_user_api.route("/authors/<user_id>/posts", methods=["GET"])
def list_post_by_user_controller(user_id):
    try:
        cursor = request.args.get('cursor')
        if cursor is not None:
            cursor = int(cursor)

        posts = list_post_by_user(user_id, cursor)

        for i in range(len(posts)):
            posts[i] = ListPostSchema().load(posts[i]._mapping)

        if len(posts) > 0:
            next_cursor = posts[-1]['id']
        else:
            next_cursor = ""

        return make_response(jsonify({
            "data": posts,
            "next_cursor": next_cursor,
        }), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": str(e)}), 500)
