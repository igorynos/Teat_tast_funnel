import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Users(Base):
    __tablename__= 'user_info'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True))
    status = Column(String, default='alive')
    status_updated_at = Column(DateTime(timezone=True))



db_path = 'db.sqlite3'
if not os.path.exists(db_path):
    engine = create_engine(f'sqlite:///{db_path}')
    
    Base.metadata.create_all(engine)
