from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API - Sumarização de Avaliações de Restaurantes")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/restaurantes/", response_model=schemas.Restaurante)
def create_restaurante(restaurante: schemas.RestauranteCreate, db: Session = Depends(get_db)):
    return crud.create_restaurante(db=db, restaurante=restaurante)

@app.get("/restaurantes/", response_model=List[schemas.Restaurante])
def read_restaurantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_restaurantes(db, skip=skip, limit=limit)

@app.post("/avaliacoes/", response_model=schemas.Avaliacao)
def create_avaliacao(avaliacao: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    return crud.create_avaliacao(db=db, avaliacao=avaliacao)

@app.get("/avaliacoes/", response_model=List[schemas.Avaliacao])
def read_avaliacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_avaliacoes(db, skip=skip, limit=limit)
