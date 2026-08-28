from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    number = Column(Integer)
    position = Column(String)
    photo_url = Column(String, nullable=True)
    
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    
    rating = Column(Float, default=0.0)

class NewsItem(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
