import os

import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

URL = "https://0ce0e595159c.ngrok.io"

FB_CLIENT_ID = os.environ.get("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.environ.get("FB_CLIENT_SECRET")
GG_CLIENT_ID = os.environ.get("GG_CLIENT_ID")
GG_CLIENT_SECRET = os.environ.get("GG_CLIENT_SECRET")

FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
GG_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GG_TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"

FB_SCOPE = ["email"]
GG_SCOPE = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from ..model.user import User
from ....helpers.jwt_token import generate_token

def get_auth_social(provider):
    if provider == "facebook":
        authorize_url = get_auth_url_fb()
    elif provider == "google":
        authorize_url = get_auth_url_gg()
    else:
        return Exception("cannot get " + provider + " auth url"), ""
    return None, authorize_url

def login_with_social(path, provider):
    if provider == "facebook":
        email = handle_fb_callback(path)
    elif provider == "google":
        email = handle_gg_callback(path)
    else:
        return Exception("invalid provider"), ""

    error, user = create_or_get_user(email, provider)
    if error is not None:
        return error, ""

    return None, generate_token({"id": user.id})

def get_auth_url_fb():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID,
        redirect_uri=URL + "/v1/facebook/callback",
        scope=FB_SCOPE,
    )
    authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)

    return authorization_url

def get_auth_url_gg():
    google = requests_oauthlib.OAuth2Session(
        GG_CLIENT_ID,
        redirect_uri=URL + "/v1/google/callback",
        scope=GG_SCOPE,
    )
    authorization_url, _ = google.authorization_url(
        GG_AUTHORIZATION_BASE_URL,
        access_type="offline",
        prompt="select_account"
    )

    return authorization_url

def handle_fb_callback(path):
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID,
        scope=FB_SCOPE,
        redirect_uri=URL + "/v1/facebook/callback",
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
        "https://graph.facebook.com/me?fields=id,email"
    ).json()

    email = facebook_user_data.get("email")

    return email

def handle_gg_callback(path):
    google = requests_oauthlib.OAuth2Session(
        GG_CLIENT_ID,
        redirect_uri=URL + "/v1/google/callback",
        scope=GG_SCOPE,
    )

    # get access token
    google.fetch_token(
        GG_TOKEN_URL,
        client_secret=GG_CLIENT_SECRET,
        authorization_response=URL + path,
    )

    # Fetch a user resource
    google_user_data = google.get(
        "https://www.googleapis.com/oauth2/v1/userinfo"
    ).json()

    email = google_user_data.get("email")

    return email


def create_or_get_user(email, provider):
    exist_user = User.query.filter_by(email=email).first()
    if exist_user is not None:
        if exist_user["provider"] != provider:
            return Exception("email is already existed"), None
        else:
            return None, exist_user

    user = User(
        provider=provider,
        email=email,
    ).create()

    return None, user
