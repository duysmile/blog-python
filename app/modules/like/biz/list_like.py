import os
from datetime import datetime

from ..model.like import Like
from ...user.model.user import User, GgInfo, FbInfo

def list_all_like_by_post(post_id, cursor):
    sql = Like.query.filter_by(post_id=post_id)
    if cursor is not None:
        dt_object = datetime.fromtimestamp(cursor)
        sql = sql.filter(Like.created_on < dt_object)

    likes = sql.order_by(Like.created_on.desc()).limit(10).all()

    if len(likes) == 0:
        return [], []

    user_ids = []
    for i in range(len(likes)):
        user_ids.append(likes[i].user_id)

    gg_user_ids = []
    fb_user_ids = []

    users = User.query.filter(User.id.in_(user_ids)).all()
    for user in users:
        provider = user.provider.value
        if provider == "facebook":
            fb_user_ids.append(user.id)
        elif provider == "google":
            gg_user_ids.append(user.id)

    gg_info = GgInfo.query.filter(GgInfo.user_id.in_(gg_user_ids)).all()
    fb_info = FbInfo.query.filter(GgInfo.user_id.in_(gg_user_ids)).all()

    names = []
    for info in gg_info:
        names.append(info.name)

    for info in fb_info:
        names.append(info.name)

    return names, likes
