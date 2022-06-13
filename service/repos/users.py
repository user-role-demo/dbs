from sqlalchemy.exc import IntegrityError

from service.db import db_session
from service.errors import ConflictError, NotFoundError
from service.models import Ability, Role, User


class UsersRepo:
    name = 'user'

    def add(self, username: str) -> User:
        try:
            user = User(name=username)
            db_session.add(user)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return user

    def get_by_uid(self, uid: int) -> User:
        user = User.query.filter(User.uid == uid).first()
        if not user:
            raise NotFoundError(self.name)
        return user

    def get_all(self) -> list[User]:
        return User.query.all()

    def update(self, uid: int, new_name: str) -> User:
        user = self.get_by_uid(uid)
        try:
            user.name = new_name
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return user

    def delete(self, uid: int) -> None:
        user = self.get_by_uid(uid)
        abilities = db_session.query(Ability).filter(Ability.user_id == uid)
        for ability in abilities:
            db_session.delete(ability)
        db_session.delete(user)
        db_session.commit()

    def add_role(self, user_id: int, role_id: int) -> Role:
        try:
            ability = Ability(user_id=user_id, role_id=role_id)
            db_session.add(ability)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return Role.query.filter(Role.uid == role_id).first()

    def get_roles(self, uid: int) -> list[Role]:
        self.get_by_uid(uid)
        return db_session.query(Role).join(Ability).filter(Ability.user_id == uid)

    def delete_role(self, user_id: int, role_id: int) -> None:
        ability = Ability.query.filter(
            Ability.user_id == user_id,
            Ability.role_id == role_id,
        ).first()
        if not ability:
            raise NotFoundError(self.name)
        db_session.delete(ability)
        db_session.commit()
