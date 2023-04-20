import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

DATABASE_URL = "sqlite:///./database.db"

# Create a SQLAlchemy engine
Engine = _sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# Create a declarative base class for database models
Base = _declarative.declarative_base()
