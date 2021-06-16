from app.modules.auth.transport.register import auth_api

def init_route(app):
    app.register_blueprint(auth_api, url_prefix="/v1")