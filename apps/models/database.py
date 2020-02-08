from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from apps.models.user import User

engine = create_engine('sqlite:///flask-jwt-auth.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_name = 'flask-jwt-auth'

db_sessions = {db_name: db_session}
db_engines = {db_name: engine}

def init_db():
    from apps.models import Base
    from apps.models.user import User

    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)

def get_session(db_name):
    session = db_sessions.get(db_name)
    if session is None:
        return 'Error'
    return session

def init_create_user():
    session = get_session('flask-jwt-auth')
    try:
        user = User(
            username='test_user_1',
            password='test',
            email='test@test.com'
        )
        session.add(user)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()

