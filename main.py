from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

app = _fastapi.FastAPI()

@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")
    user = await _services.create_user(user, db)
    return await _services.create_token(user)

@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

@app.post("/api/tasks", response_model=_schemas.Task)
async def create_task(
    task: _schemas.TaskCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return await _services.create_task(task, current_user, db)

@app.get("/api/tasks/{task_id}", response_model=_schemas.Task)
async def get_task(
    task_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return await _services.get_task(task_id, db)

@app.get("/api/tasks", response_model=List[_schemas.Task])
async def get_tasks(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return await _services.get_tasks(current_user.id, db)

@app.put("/api/tasks/{task_id}", response_model=_schemas.Task)
async def update_task(
    task_id: int,
    task: _schemas.TaskCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return await _services.update_task(task_id, task, current_user.id, db)

@app.delete("/api/tasks/{task_id}", response_model=_schemas.Task)
async def delete_task(
    task_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    current_user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return await _services.delete_task(task_id, current_user.id, db)