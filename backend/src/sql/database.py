import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connect_args = None
if 'sqlite' in os.environ["SQLALCHEMY_DATABASE_URI"]:
    connect_args = {"check_same_thread": False}

engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"], connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
