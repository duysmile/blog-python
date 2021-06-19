from flask import Blueprint, request, jsonify, make_response
import logging

from ..biz.register_biz import login_with_social, get_auth_social

auth_api = Blueprint("authentication", __name__)

@auth_api.route("/login/<provider>", methods=["POST"])
def login(provider):
    try:
        if provider is None:
            return make_response(jsonify({"data": "must provide provider"}), 400)

        error, authorize_url = get_auth_social(provider)
        if error is not None:
            return make_response(jsonify({"error": "must provide provider"}), 400)

        return make_response(jsonify({"data": authorize_url}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": "cannot create " + provider+ " auth url"}), 500)


@auth_api.route("/<provider>/callback", methods=["GET", "POST"])
def social_callback(provider):
    try:
        error, token = login_with_social(request.full_path, provider)
        if error is not None:
            return make_response(jsonify({"error": str(error)}), 400)
        return make_response(jsonify({"data": token}), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"error": "cannot register user"}), 500)

