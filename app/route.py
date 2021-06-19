from app.modules.user.transport.register import auth_api
from app.modules.user.transport.update_profile import user_api
from app.modules.post.transport.create_post import create_post_api
from app.modules.post.transport.list_post import list_post_api
from app.modules.post.transport.list_post_by_user import list_post_by_user_api
from app.modules.like.transport.like_post import like_post_api
from app.modules.post.transport.get_post import get_post_api
from app.modules.like.transport.list_like import list_like_by_post_api

def init_route(app):
    app.register_blueprint(auth_api, url_prefix="/v1")
    app.register_blueprint(user_api, url_prefix="/v1/me")
    app.register_blueprint(create_post_api, url_prefix="/v1/posts")
    app.register_blueprint(list_post_api, url_prefix="/v1/posts")
    app.register_blueprint(list_post_by_user_api, url_prefix="/v1")
    app.register_blueprint(like_post_api, url_prefix="/v1")
    app.register_blueprint(list_like_by_post_api, url_prefix="/v1")
    app.register_blueprint(get_post_api, url_prefix="/v1/posts")