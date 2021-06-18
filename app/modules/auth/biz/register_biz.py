import os

import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

URL = "https://0ce0e595159c.ngrok.io"

FB_CLIENT_ID = os.environ.get("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.environ.get("FB_CLIENT_SECRET")

FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

FB_SCOPE = ["email"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from ..model.user import User

def get_auth_url_fb():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, redirect_uri=URL + "/v1/fb-callback", scope=FB_SCOPE
    )
    authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)

    return authorization_url

def handle_fb_callback(path):
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL + "/v1/fb-callback"
    )

    # we need to apply a fix for Facebook here
    facebook = facebook_compliance_fix(facebook)

    # get access token
    facebook.fetch_token(
        FB_TOKEN_URL,
        client_secret=FB_CLIENT_SECRET,
        authorization_response=URL + path,
    )

    # Fetch a user resource
    facebook_user_data = facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    email = facebook_user_data.get("email")

    return email

def create_user(email, provider):
    exist_user = User.query.filter_by(email=email).first()
    if exist_user is not None:
        return Exception("email is already existed")

    User(
        provider=provider,
        email=email,
    ).create()

    return None


