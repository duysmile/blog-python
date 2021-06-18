import jwt
import os

SECRET_KEY = os.environ["SECRET_KEY_JWT"]

def generate_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])