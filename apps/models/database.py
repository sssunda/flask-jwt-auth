from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///flask-jwt-auth.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_name = 'flask-jwt-auth'

Base = declarative_base()
Base.query = db_session.query_property()

db_sessions = {db_name: db_session}
db_engines = {db_name: engine}

def init_db():
    from models.user import User
    Base.metadata.create_all(engine)


def get_session(db_name):
    session = db_sessions.get(db_name)
    if session is None:
        return 'Error'
    return session
