from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phoenix Team API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_admin(admin_token: str = Header(default="")):
    if admin_token != "phoenix_admin_secret":
        raise HTTPException(status_code=403, detail="Доступ запрещен. Нужны права разработчика.")

# Стартовая инициализация базы данных первым игроком
@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    if not db.query(models.Player).first():
        first_player = models.Player(
            full_name="Андрей Давидонис", 
            number=1, 
            position="Вратарь",
            saves=0
        )
        db.add(first_player)
        db.commit()
    db.close()

@app.get("/players/", response_model=List[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Player).offset(skip).limit(limit).all()

@app.post("/players/", response_model=schemas.Player, dependencies=[Depends(verify_admin)])
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = models.Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@app.get("/news/", response_model=List[schemas.NewsItem])
def read_news(db: Session = Depends(get_db)):
    return db.query(models.NewsItem).order_by(models.NewsItem.created_at.desc()).all()

@app.post("/news/", response_model=schemas.NewsItem, dependencies=[Depends(verify_admin)])
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = models.NewsItem(**news.model_dump())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news
