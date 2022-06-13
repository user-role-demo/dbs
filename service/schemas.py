from pydantic import BaseModel, constr


class User(BaseModel):
    uid: int
    name: constr(min_length=1)  # type: ignore

    class Config:
        orm_mode = True


class Role(BaseModel):
    uid: int
    name: constr(min_length=1)  # type: ignore

    class Config:
        orm_mode = True


class Ability(BaseModel):
    uid: int
    user_id: int
    role_id: int

    class Config:
        orm_mode = True
