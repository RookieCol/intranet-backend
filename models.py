import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash 
import database as _database

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    created_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    updated_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow())
    tasks = _orm.relationship("Task", back_populates="owner")
 
    def verify_password(self, password:str):
        return _hash.bcrypt.verify(password, self.hashed_password)
    

class Task(_database.Base):
    __tablename__ = "tasks"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    note = _sql.Column(_sql.String,default="")
    created_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    last_update = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow())
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    owner = _orm.relationship("User", back_populates="tasks")
