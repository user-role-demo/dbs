from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from service import schemas
from service.repos.roles import RolesRepo

role_view = Blueprint('role_view', __name__)

repo = RolesRepo()


@role_view.post('/')
def add_role():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'The body of the request could not be empty')

    payload['uid'] = -1
    role = schemas.Role(**payload)
    entity = repo.add(rolename=role.name)
    new_role = schemas.Role.from_orm(entity)
    return new_role.dict(), HTTPStatus.CREATED


@role_view.get('/')
def get_roles():
    entities = repo.get_all()
    roles = [schemas.Role.from_orm(entity).dict() for entity in entities]
    return jsonify(roles), HTTPStatus.OK


@role_view.get('/<uid>')
def get_role_by_id(uid: int):
    entity = repo.get_by_uid(uid)
    role = schemas.Role.from_orm(entity)
    return role.dict(), HTTPStatus.OK


@role_view.put('/<uid>')
def update_role(uid: int):
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'The body of the request could not be empty')

    payload['uid'] = uid
    role = schemas.Role(**payload)
    entity = repo.update(uid=uid, new_name=role.name)
    updated_role = schemas.Role.from_orm(entity)
    return updated_role.dict(), HTTPStatus.OK


@role_view.delete('/<uid>')
def delete_role(uid: int):
    repo.delete(uid)
    return {}, HTTPStatus.NO_CONTENT
