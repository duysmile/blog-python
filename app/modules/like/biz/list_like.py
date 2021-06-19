import os

from ..model.post import Post

def list_all_post(cursor):
    sql = Post.query
    if cursor is not None and cursor > 0:
        sql = sql.filter(Post.id < cursor)

    return sql.order_by(Post.id.desc()).limit(10).all()

def list_post_by_user(user_id, cursor):
    sql = Post.query.filter_by(author_id=user_id)
    if cursor is not None and cursor > 0:
        sql = sql.filter(Post.id < cursor)

    return sql.order_by(Post.id.desc()).limit(10).all()
