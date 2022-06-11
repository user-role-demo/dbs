from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from service.db import Base, engine


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(), unique=True)

    def __str__(self) -> str:
        return f'User {self.uid}, {self.name}'


class Role(Base):
    __tablename__ = 'roles'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(), unique=True)

    def __str__(self) -> str:
        return f'Role {self.uid}, {self.name}'


class UserRole(Base):
    __tablename__ = 'user_roles'
    uid = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.uid), nullable=False)
    role_id = Column(Integer, ForeignKey(Role.uid), nullable=False)
    user = relationship('User', lazy='joined')
    role = relationship('Role', lazy='joined')

    def __repr__(self) -> str:
        return f'UserRole user: {self.user_id} role: {self.role_id}'


def create_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    create_db()
