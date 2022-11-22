import fastapi
from fastapi import security

import database
from sqlalchemy import orm
from passlib import hash
import jwt

import schemas
import models

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")

secret = "mysecret"


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def create_user(user: schemas.UserCreate, db: orm.Session):
    user_obj = models.User(
        email=user.email, hashed_password=hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return user_obj


async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(email, db)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), secret)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")

    return schemas.User.from_orm(user)


async def create_task(user: schemas.User, db: orm.Session, task: schemas.TaskCreate):
    task = models.Task(**task.dict(), user_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return schemas.Task.from_orm(task)


async def get_tasks(user: schemas.User, db: orm.Session):
    tasks = db.query(models.Task).filter_by(user_id=user.id).order_by(models.Task.id)

    return list(map(schemas.Task.from_orm, tasks))


async def _task_selector(task_id: int, user: schemas.User, db: orm.Session):
    task = (
        db.query(models.Task)
        .filter_by(user_id=user.id)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise fastapi.HTTPException(status_code=404, detail="Task does not exist")

    return task


async def get_task(task_id: int, user: schemas.User, db: orm.Session):
    task = await _task_selector(task_id, user, db)

    return schemas.Task.from_orm(task)


async def delete_task(task_id: int, user: schemas.User, db: orm.Session):
    task = await _task_selector(task_id, user, db)

    db.delete(task)
    db.commit()


async def update_task(
    task_id: int, task: schemas.TaskCreate, user: schemas.User, db: orm.Session
):
    task_db = await _task_selector(task_id, user, db)

    task_db.title = task.title
    task_db.description = task.description
    task_db.priority = task.priority
    task_db.progress = task.progress
    task_db.status = task.status

    db.commit()
    db.refresh(task_db)

    return schemas.Task.from_orm(task_db)
