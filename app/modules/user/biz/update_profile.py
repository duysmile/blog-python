import os

from ..model.user import FbInfo, GgInfo

def create_or_update_profile(id, provider, data):
    exist_info = find_profile(id, provider)
    if exist_info is not None:
        update_profile(id, provider, data)
        return

    create_profile(id, provider, data)

def update_profile(id, provider, data):
    if provider == "facebook":
        FbInfo.update(user_id=id, data={
            "name": data['name'],
            "phone_number": data['phone_number'],
        })
    elif provider == "google":
        GgInfo.update(user_id=id, data={
            "name": data['name'],
            "occupation": data['occupation'],
        })

def create_profile(id, provider, data):
    if provider == "facebook":
        FbInfo(
            user_id=id,
            name=data['name'],
            phone_number=data['phone_number'],
        ).create()
    elif provider == "google":
        GgInfo(
            user_id=id,
            name=data['name'],
            occupation=data['occupation'],
        ).create()

def find_profile(id, provider):
    if provider == "facebook":
        return FbInfo.query.filter_by(user_id=id).first()
    elif provider == "google":
        return GgInfo.query.filter_by(user_id=id).first()

    return None
