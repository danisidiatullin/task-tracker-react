import sqlalchemy.orm as orm
from passlib import hash
from sqlalchemy import Column, Integer, String, ForeignKey, types

import database
from schemas import StatusEnum


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class Task(database.Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, unique=True, index=True)
    description = Column(String)
    priority = Column(Integer)
    progress = Column(Integer)

    status = Column(
        ChoiceType({e.name: e.value for e in StatusEnum}), nullable=True
    )

    user = orm.relationship("User", back_populates="tasks")


class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    tasks = orm.relationship("Task", back_populates="user")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)



