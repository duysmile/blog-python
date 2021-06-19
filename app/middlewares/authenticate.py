from flask import request, jsonify, make_response
from functools import wraps

from ..helpers.jwt_token import verify_token
from ..modules.user.model.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "authorization" in request.headers:
            token = request.headers["authorization"]
        # return 401 if token is not passed
        if not token:
            return make_response(jsonify({"error" : "token is missing"}), 401)

        try:
            # decoding the payload to fetch the stored details
            token = token.split("Bearer ")
            if len(token) == 2:
                token = token[1]
            else:
                return make_response(jsonify({"error" : "invalid token"}), 401)
            data = verify_token(token)
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            return make_response(jsonify({"error" : "invalid token"}), 401)
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)

    return decorated

def user_required_info():
    pass