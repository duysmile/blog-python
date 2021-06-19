from app.modules.user.transport.register import auth_api
from app.modules.user.transport.update_profile import user_api

def init_route(app):
    app.register_blueprint(auth_api, url_prefix="/v1")
    app.register_blueprint(user_api, url_prefix="/v1/me")