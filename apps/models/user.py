from sqlalchemy import Column, Integer, String, DateTime, Boolean
from apps.models import Base
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, unique=False, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email
        self.set_password(password)
        if kwargs.get('is_staff', ''):
            self.is_staff = kwargs['is_staff']
        if kwargs.get('is_active', ''):
            self.is_active = kwargs['is_active']

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')


    def check_password(self, password):
        return check_password_hash(self.password, password)

