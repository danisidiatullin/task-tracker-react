from enum import Enum

import pydantic


class UserBase(pydantic.BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class StatusEnum(str, Enum):
    started = "started"
    pending = "pending"
    finished = "finished"


class TaskBase(pydantic.BaseModel):
    title: str
    description: str
    priority: int
    progress: int
    status: StatusEnum = StatusEnum.started


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
