from app.modules.user.transport.register import auth_api
from app.modules.user.transport.update_profile import user_api
from app.modules.post.transport.create_post import create_post_api

def init_route(app):
    app.register_blueprint(auth_api, url_prefix="/v1")
    app.register_blueprint(user_api, url_prefix="/v1/me")
    app.register_blueprint(create_post_api, url_prefix="/v1/posts")