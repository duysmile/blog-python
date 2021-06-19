from flask import Blueprint, request, jsonify, make_response
import logging

from ..biz.list_post import list_all_post

list_post_api = Blueprint("list_all_posts", __name__)

@list_post_api.route("", methods=["GET"])
def list_all_post_controller():
    try:
        cursor = request.args.get('cursor')
        if cursor is not None:
            cursor = int(cursor)

        posts = list_all_post(cursor)

        if len(posts) > 0:
            next_cursor = posts[-1].id
        else:
            next_cursor = ""

        return make_response(jsonify({
            "data": posts,
            "next_cursor": next_cursor,
        }), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": str(e)}), 500)
