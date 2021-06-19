import os

from ..model.post import Post
from ...user.model.user import User, FbInfo, GgInfo
from ...like.model.like import Like

def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    provider = post.author.provider.value
    author_id = post.author_id
    author_info = None
    if provider == "facebook":
        author_info = FbInfo.query.filter_by(user_id=author_id).first()
    elif provider == "google":
        author_info = GgInfo.query.filter_by(user_id=author_id).first()

    likes = Like.query.filter_by(post_id=post_id).count()
    last_likes = Like.query.filter_by(post_id=post_id).limit(2).all()
    last_ids = []
    for i in range(len(last_likes)):
        last_ids[i] = last_likes[i].user_id

    users_like = User.query.filter(User.id.in_(last_ids)).all()
    arr_user = []
    for i in range(len(users_like)):
        id = users_like[i].id
        provider = users_like[i].provider.value
        user = None
        if provider == "facebook":
            user = FbInfo.query.filter_by(user_id=id).first()
        if provider == "google":
            user = GgInfo.query.filter_by(user_id=id).first()

        arr_user.append(user.name)

    remain_like = likes - 2
    like_str = ",".join(arr_user)
    if remain_like > 0:
        like_str += str(remain_like)
    elif likes == 0:
        like_str += "No one"

    like_str += " like(s) this post"

    return {
        "title": post.title,
        "summary": post.summary,
        "content": post.content,
        "author": author_info.name,
        "likes": like_str,
    }

