from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import SessionLocal, engine

# Cria as tabelas conforme os models novos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API - Sumarização de Avaliações de Restaurantes (Nova Estrutura)")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- Restaurantes -----
@app.post("/restaurantes/", response_model=schemas.Restaurante)
def create_restaurante(restaurante: schemas.RestauranteCreate, db: Session = Depends(get_db)):
    return crud.create_restaurante(db, restaurante)

@app.get("/restaurantes/", response_model=List[schemas.Restaurante])
def read_restaurantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_restaurantes(db, skip=skip, limit=limit)

# ----- Clientes -----
@app.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db, cliente)

@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clientes(db, skip=skip, limit=limit)

# ----- Comentários -----
@app.post("/comentarios/", response_model=schemas.Comentario)
def create_comentario(comentario: schemas.ComentarioCreate, db: Session = Depends(get_db)):
    return crud.create_comentario(db, comentario)

@app.get("/comentarios/", response_model=List[schemas.Comentario])
def read_comentarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_comentarios(db, skip=skip, limit=limit)

# ----- Categorias de Opinião -----
@app.post("/categorias-opiniao/", response_model=schemas.CategoriaOpiniao)
def create_categoria_opiniao(cat: schemas.CategoriaOpiniaoCreate, db: Session = Depends(get_db)):
    return crud.create_categoria_opiniao(db, cat)

@app.get("/categorias-opiniao/", response_model=List[schemas.CategoriaOpiniao])
def read_categorias_opiniao(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categorias_opiniao(db, skip=skip, limit=limit)

# ----- Opiniões -----
@app.post("/opinioes/", response_model=schemas.Opiniao)
def create_opiniao(opiniao: schemas.OpiniaoCreate, db: Session = Depends(get_db)):
    return crud.create_opiniao(db, opiniao)

@app.get("/opinioes/", response_model=List[schemas.Opiniao])
def read_opinioes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_opinioes(db, skip=skip, limit=limit)

# ----- Comparação (mantida) -----
@app.get("/comparar_aspectos", response_model=List[schemas.AspectoComparado])
def comparar_aspectos(restaurante1_id: int, restaurante2_id: int, db: Session = Depends(get_db)):
    return crud.comparar_aspectos(db, restaurante1_id, restaurante2_id)
