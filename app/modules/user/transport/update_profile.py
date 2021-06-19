from flask import Blueprint, request, jsonify, make_response
import flask
import logging

from app.modules.user.model.user import User, FbInfoSchema, GgInfoSchema
from ..biz.update_profile import create_or_update_profile
from ....middlewares.authenticate import token_required

user_api = Blueprint("/me", __name__)

@user_api.route("/profile", methods=["POST"])
@token_required
def login(current_user):
    try:
        data = request.get_json()
        provider = current_user.provider.value
        if provider == "facebook":
            data = FbInfoSchema().load(data)
        elif provider == "google":
            data = GgInfoSchema().load(data)
        else:
            return make_response(jsonify({"error": "unknown provider"}), 400)

        create_or_update_profile(current_user.id, provider, data)
        return make_response(jsonify({"data": True}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": "cannot update user"}), 500)
