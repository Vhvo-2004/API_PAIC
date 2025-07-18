from sqlalchemy.orm import Session
import models, schemas

def create_restaurante(db: Session, restaurante: schemas.RestauranteCreate):
    db_restaurante = models.Restaurante(**restaurante.dict())
    db.add(db_restaurante)
    db.commit()
    db.refresh(db_restaurante)
    return db_restaurante

def get_restaurantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurante).offset(skip).limit(limit).all()

def create_avaliacao(db: Session, avaliacao: schemas.AvaliacaoCreate):
    db_avaliacao = models.Avaliacao(**avaliacao.dict())
    db.add(db_avaliacao)
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao

def get_avaliacoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Avaliacao).offset(skip).limit(limit).all()
