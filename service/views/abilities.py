from http import HTTPStatus

from flask import Blueprint, jsonify, request

from service import schemas
from service.repos.abilities import AbilitiesRepo

ability_view = Blueprint('ability_view', __name__)

repo = AbilitiesRepo()


@ability_view.post('/')
def add_ability():
    payload = request.json
    payload['uid'] = -1
    ability = schemas.Ability(**payload)
    entity = repo.add(user_id=ability.user_id, role_id=ability.role_id)
    new_ability = schemas.Ability.from_orm(entity)
    return new_ability.dict(), HTTPStatus.CREATED


@ability_view.get('/')
def get_abilities():
    entities = repo.get_all()
    abilities = [schemas.Ability.from_orm(entity).dict() for entity in entities]
    return jsonify(abilities), HTTPStatus.OK


@ability_view.get('/<uid>')
def get_ability_by_id(uid: int):
    entity = repo.get_by_uid(uid)
    ability = schemas.Ability.from_orm(entity)
    return ability.dict(), HTTPStatus.OK


@ability_view.put('/<uid>')
def update_ability(uid: int):
    payload = request.json
    payload['uid'] = uid
    ability = schemas.Ability(**payload)
    entity = repo.update(**ability.dict())
    updated_ability = schemas.Ability.from_orm(entity)
    return updated_ability.dict(), HTTPStatus.OK


@ability_view.delete('/<uid>')
def delete_ability(uid: int):
    repo.delete(uid)
    return {}, HTTPStatus.NO_CONTENT
