import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database, models as _models, schemas as _schemas

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"


def create_database():
    return _database.Base.metadata.create_all(bind=_database.Engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).one_or_none()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    db_user = await get_user_by_email(user.email, db)
    if db_user is None:
        user_obj = _models.User(
            email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password)
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj
    else:
        raise _fastapi.HTTPException(
            status_code=400, detail="User with this email already exists."
        )

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    token = _jwt.encode(_schemas.User.from_orm(user).dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)


async def create_task(task: _schemas.TaskCreate, user: _schemas.User, db: _orm.Session):
    current_time = _dt.datetime.utcnow()
    task_obj = _models.Task(**task.dict(), owner_id=user.id, created_at=current_time, last_update=current_time)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return _schemas.Task.from_orm(task_obj)

async def get_task(task_id: int, db: _orm.Session):
    task = db.query(_models.Task).filter(_models.Task.id == task_id).one_or_none()
    if task:
        return _schemas.Task.from_orm(task)
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Task not found")

async def get_tasks(user_id: int, db: _orm.Session):
    tasks = db.query(_models.Task).filter(_models.Task.owner_id == user_id).all()
    return [_schemas.Task.from_orm(task) for task in tasks]

async def update_task(task_id: int, task: _schemas.TaskCreate, user_id: int, db: _orm.Session):
    current_task = db.query(_models.Task).filter(_models.Task.id == task_id, _models.Task.owner_id == user_id).one_or_none()

    if current_task:
        current_task.name = task.name
        current_task.note = task.note
        current_task.last_update = _dt.datetime.utcnow()

        db.commit()
        db.refresh(current_task)

        return _schemas.Task.from_orm(current_task)
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Task not found")

async def delete_task(task_id: int, user_id: int, db: _orm.Session):
    task = db.query(_models.Task).filter(_models.Task.id == task_id, _models.Task.owner_id == user_id).one_or_none()

    if task:
        db.delete(task)
        db.commit()
        return _schemas.Task.from_orm(task)
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Task not found")