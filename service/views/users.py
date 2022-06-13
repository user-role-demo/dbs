from http import HTTPStatus

from flask import Blueprint, jsonify, request

from service import schemas
from service.repos.users import UsersRepo

user_view = Blueprint('user_view', __name__)

repo = UsersRepo()


@user_view.post('/')
def add_user():
    payload = request.json
    payload['uid'] = -1
    user = schemas.User(**payload)
    entity = repo.add(username=user.name)
    new_user = schemas.User.from_orm(entity)
    return new_user.dict(), HTTPStatus.CREATED


@user_view.get('/')
def get_users():
    entities = repo.get_all()
    users = [schemas.User.from_orm(entity).dict() for entity in entities]
    return jsonify(users), HTTPStatus.OK


@user_view.get('/<uid>')
def get_user_by_id(uid: int):
    entity = repo.get_by_uid(uid)
    user = schemas.User.from_orm(entity)
    return user.dict(), HTTPStatus.OK


@user_view.put('/<uid>')
def update_user(uid: int):
    payload = request.json
    payload['uid'] = uid
    user = schemas.User(**payload)
    entity = repo.update(uid=uid, new_name=user.name)
    updated_user = schemas.User.from_orm(entity)
    return updated_user.dict(), HTTPStatus.OK


@user_view.delete('/<uid>')
def delete_user(uid: int):
    repo.delete(uid)
    return {}, HTTPStatus.NO_CONTENT


@user_view.post('/<user_id>/roles')
def add_role(user_id: int):
    payload = request.json
    payload['uid'] = -1
    payload['user_id'] = user_id
    ability = schemas.Ability(**payload)
    entity = repo.add_role(user_id=user_id, role_id=ability.role_id)
    new_role = schemas.Role.from_orm(entity)
    return new_role.dict(), HTTPStatus.CREATED


@user_view.get('/<user_id>/roles')
def get_roles(user_id: int):
    entities = repo.get_roles(uid=user_id)
    roles = [schemas.Role.from_orm(entity).dict() for entity in entities]
    return jsonify(roles), HTTPStatus.OK


@user_view.delete('/<user_id>/roles/<role_id>')
def delete_role(user_id: int, role_id: int):
    repo.delete_role(user_id=user_id, role_id=role_id)
    return {}, HTTPStatus.NO_CONTENT
