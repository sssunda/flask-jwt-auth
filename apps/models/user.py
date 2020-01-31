from sqlalchemy import Column, Integer, String, DateTime
from models.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

