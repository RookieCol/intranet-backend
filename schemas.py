import datetime as _dt
import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class config:
        orm_mode = True


class User(_UserBase):
    id: int
    created_at: _dt.datetime
    updated_at: _dt.datetime
    leads: list = []

    class config:
        orm_mode = True


class _LeadBase(_pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str


class LeadCreated(_LeadBase):
    pass


class Lead(_LeadBase):
    id: int
    created_at: _dt.datetime
    last_update: _dt.datetime
    owner_id: int

    class config:
        orm_mode = True