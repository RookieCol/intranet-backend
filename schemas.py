import datetime as _dt
import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    email: str

class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True

class _TaskBase(_pydantic.BaseModel):
    name: str
    note: str

class TaskCreate(_TaskBase):
    pass

class Task(_TaskBase):
    id: int
    owner_id: int
    created_at: _dt.datetime  # Updated field name
    last_update: _dt.datetime  # Updated field name

    class Config:
        orm_mode = True
