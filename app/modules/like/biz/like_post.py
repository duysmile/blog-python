import os

from ..model.like import Like

def like_post(like):
    exist_post = find_like(like)
    if exist_post is not None:
        return

    Like(
        user_id=like["user_id"],
        post_id=like["post_id"],
    ).create()

def unlike_post(like):
    exist_post = find_like(like)
    if exist_post is None:
        return

    Like.delete(exist_post)

def find_like(like):
    return Like.query.filter_by(user_id=like["user_id"], post_id=like["post_id"]).first()
