import fastapi as _fastapi
import sqlalchemy.orm as _orm
import fastapi.security as _security
import services as _services, schemas as _schemas

app = _fastapi()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/api/users")
async def create_user(user:_schemas.UserCreate, db: _orm.session = _fastapi.Depends()):
    pass


