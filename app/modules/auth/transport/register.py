from flask import Blueprint, request, jsonify, make_response
from app.modules.auth.model.user import User

auth_api = Blueprint("authentication", __name__)

@auth_api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user = User(
        provider=data["provider"],
        email=data["email"],
    ).create()
    return make_response(jsonify({"data": True}), 200)
