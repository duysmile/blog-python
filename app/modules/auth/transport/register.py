from flask import Blueprint, request, jsonify, make_response
import flask
import logging

from app.modules.auth.model.user import User
from ..biz.register_biz import get_auth_url_fb, handle_fb_callback, create_user, get_auth_url_gg, handle_gg_callback

auth_api = Blueprint("authentication", __name__)

@auth_api.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        provider = data["provider"]
        if provider is None:
            return make_response(jsonify({"data": "must provide provider"}), 400)

        authorize_url = ""
        if provider == "facebook":
            authorize_url = get_auth_url_fb()
        elif provider == "google":
            authorize_url = get_auth_url_gg()
        else:
            return make_response(jsonify({"error": "must provide provider"}), 400)

        return make_response(jsonify({"data": authorize_url}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": "cannot create auth url for facebook"}), 500)


@auth_api.route("/<provider>/callback", methods=["GET", "POST"])
def fb_callback(provider):
    try:
        email = ""
        if provider == "facebook":
            email = handle_fb_callback(flask.request.full_path)
        elif provider == "google":
            email = handle_gg_callback(flask.request.full_path)
        else:
            return make_response(jsonify({"error": "invalid provider"}), 400)

        error = create_user(email, provider)
        if error is not None:
            return make_response(jsonify({"error": str(error)}), 400)
        return make_response(jsonify({"data": True}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": "cannot register user"}), 500)

