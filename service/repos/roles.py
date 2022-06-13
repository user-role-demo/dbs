from sqlalchemy.exc import IntegrityError

from service.db import db_session
from service.errors import ConflictError, NotFoundError
from service.models import Ability, Role, User


class RolesRepo:
    name = 'role'

    def add(self, rolename: str) -> Role:
        try:
            role = Role(name=rolename)
            db_session.add(role)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return role

    def get_by_uid(self, uid: int) -> Role:
        role = Role.query.filter(Role.uid == uid).first()
        if not role:
            raise NotFoundError(self.name)
        return role

    def get_all(self) -> list[Role]:
        return Role.query.all()

    def update(self, uid: int, new_name: str) -> Role:
        role = self.get_by_uid(uid)
        try:
            role.name = new_name
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return role

    def delete(self, uid: int) -> None:
        role = self.get_by_uid(uid)
        abilities = db_session.query(Ability).filter(Ability.role_id == uid)
        for ability in abilities:
            db_session.delete(ability)
        db_session.delete(role)
        db_session.commit()

    def get_users(self, uid: int) -> list[User]:
        self.get_by_uid(uid)
        return db_session.query(User).join(Ability).filter(Ability.role_id == uid)
