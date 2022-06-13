from sqlalchemy.exc import IntegrityError

from service.db import db_session
from service.errors import ConflictError, NotFoundError
from service.models import Ability


class AbilitiesRepo:
    name = 'ability'

    def add(self, user_id: int, role_id: int) -> Ability:
        try:
            ability = Ability(user_id=user_id, role_id=role_id)
            db_session.add(ability)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return ability

    def get_by_uid(self, uid: int) -> Ability:
        ability = Ability.query.filter(Ability.uid == uid).first()
        if not ability:
            raise NotFoundError(self.name)
        return ability

    def get_all(self) -> list[Ability]:
        return Ability.query.all()

    def update(self, uid: int, user_id: int, role_id: int) -> Ability:
        ability = self.get_by_uid(uid)
        try:
            ability.user_id = user_id
            ability.role_id = role_id
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return ability

    def delete(self, uid: int) -> None:
        ability = self.get_by_uid(uid)
        db_session.delete(ability)
        db_session.commit()
