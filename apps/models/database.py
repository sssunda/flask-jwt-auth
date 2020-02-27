# Third Party Module Import
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app

# Python Module Import
import logging

# Apps Module Import
from apps.models.user import User
from apps.utils.get_config import get_config


database = get_config('DATABASE')
engine = create_engine(f'sqlite:///{database}', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_name = 'flask-jwt-auth'

db_sessions = {db_name: db_session}
db_engines = {db_name: engine}


def init_db():
    from apps.models import Base
    from apps.models.user import User

    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)


def get_session(db_name=db_name):
    db = db_sessions.get(db_name)
    if db is None:
        return 'Error'
    return db


def init_create_user():
    db = get_session('flask-jwt-auth')
    try:
        user = User(
            username='test_user_1',
            password='test',
            email='test@test.com'
        )
        db.add(user)
        db.commit()
    except Exception as e:
        logging.error(e)
        db.rollback()
