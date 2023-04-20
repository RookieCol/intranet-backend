from fastapi import FastAPI,Depends
import sqlalchemy.orm as _orm
import fastapi.security as _security
import services as _services, schemas as _schemas


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/api/users")
async def create_user(user: _schemas.UserCreate, db: _orm.session = Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise FastAPI.HTTPException(status_code=400, detail="Email already registered")
    return await _services.create_user(user, db)