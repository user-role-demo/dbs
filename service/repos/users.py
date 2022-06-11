from sqlalchemy.exc import IntegrityError

from service.db import db_session
from service.errors import ConflictError, NotFoundError
from service.models import User


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
        user = User.query.filter(User.uid == uid).first()
        if not user:
            raise NotFoundError(self.name)
        try:
            user.name = new_name
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return user

    def delete(self, uid: int) -> None:
        user = User.query.filter(User.uid == uid).first()
        if not user:
            raise NotFoundError(self.name)
        db_session.delete(user)
        db_session.commit()
