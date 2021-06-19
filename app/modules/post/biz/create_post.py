import os

from ..model.post import Post

def create_post_biz(author_id, data):
    exist_post = find_post(data['title'])
    if exist_post is not None:
        raise Exception("post title is already existed")

    Post(
        author_id=author_id,
        title=data['title'],
        summary=data['summary'],
        content=data['content'],
    ).create()

def find_post(title):
    return Post.query.filter_by(title=title).first()
