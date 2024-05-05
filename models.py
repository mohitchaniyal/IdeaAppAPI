from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
class Idea(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idea_name = Column(String, nullable=False)
    idea_disc = Column(String, nullable=False)
    idea_author = Column(String, nullable=False)
    public = Column(Boolean, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    owner = relationship('User')

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    phone_number = Column(String,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))

class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    idea_id = Column(Integer,ForeignKey("ideas.id",ondelete="CASCADE"),primary_key=True)