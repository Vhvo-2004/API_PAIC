from sqlalchemy.orm import Session
from sqlalchemy import func , case
import models, schemas

# ---------- CRUD básicos ----------
def create_restaurante(db: Session, restaurante: schemas.RestauranteCreate):
    obj = models.Restaurante(**restaurante.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_restaurantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurante).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    obj = models.Cliente(**cliente.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def create_comentario(db: Session, comentario: schemas.ComentarioCreate):
    obj = models.Comentario(**comentario.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_comentarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comentario).offset(skip).limit(limit).all()

def create_categoria_opiniao(db: Session, categoria: schemas.CategoriaOpiniaoCreate):
    obj = models.CategoriaOpiniao(**categoria.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_categorias_opiniao(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CategoriaOpiniao).offset(skip).limit(limit).all()

def create_opiniao(db: Session, opiniao: schemas.OpiniaoCreate):
    obj = models.Opiniao(**opiniao.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_opinioes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Opiniao).offset(skip).limit(limit).all()

def comparar_aspectos(db: Session, restaurante1_id: int, restaurante2_id: int):
    # Média de polaridade por CATEGORIA para cada restaurante (subquery)
    sub = (
        db.query(
            models.CategoriaOpiniao.categoria.label("categoria"),
            models.Comentario.restaurante_id.label("rest_id"),
            func.avg(models.Opiniao.polaridade).label("media"),
        )
        .join(models.Opiniao, models.Opiniao.categoria_id == models.CategoriaOpiniao.id)
        .join(models.Comentario, models.Comentario.id == models.Opiniao.comentario_id)
        .filter(models.Comentario.restaurante_id.in_([restaurante1_id, restaurante2_id]))
        .group_by(models.CategoriaOpiniao.categoria, models.Comentario.restaurante_id)
        .subquery()
    )

    # Pivot: 1 linha por categoria, colunas m1/m2
    rows = (
        db.query(
            sub.c.categoria,
            func.avg(case((sub.c.rest_id == restaurante1_id, sub.c.media), else_=None)).label("m1"),
            func.avg(case((sub.c.rest_id == restaurante2_id, sub.c.media), else_=None)).label("m2"),
        )
        .group_by(sub.c.categoria)
        .order_by(sub.c.categoria)
        .all()
    )

    # Constrói o payload esperado pelo app
    return [
        schemas.AspectoComparado(
            aspecto=row.categoria,
            notaPredita1=float(row.m1 or 0.0),
            notaPredita2=float(row.m2 or 0.0),
        )
        for row in rows
    ]

# --------- READS ---------
def get_chart_polaridade(db: Session, restaurante_id: int, aspecto: str | None = None):
    q = db.query(models.ChartPolaridadeAspecto).filter(
        models.ChartPolaridadeAspecto.restaurante_id == restaurante_id
    )
    if aspecto:
        q = q.filter(models.ChartPolaridadeAspecto.aspecto == aspecto)
    return q.order_by(models.ChartPolaridadeAspecto.aspecto.asc()).all()

def get_chart_genero(db: Session, restaurante_id: int, categoria_id: int | None = None):
    q = db.query(models.ChartGeneroAspecto).filter(
        models.ChartGeneroAspecto.restaurante_id == restaurante_id
    )
    if categoria_id is not None:
        q = q.filter(models.ChartGeneroAspecto.categoria_id == categoria_id)
    return q.order_by(models.ChartGeneroAspecto.categoria_id.asc()).all()

def get_chart_polaridade_categoria(db: Session, restaurante_id: int):
    return (
        db.query(models.ChartPolaridadeCategoria)
        .filter(models.ChartPolaridadeCategoria.restaurante_id == restaurante_id)
        .order_by(models.ChartPolaridadeCategoria.categoria_nome.asc())
        .all()
    )

def refresh_charts(db: Session, restaurante_id: int | None = None):
    # Se restaurante_id for None, recomputa tudo; senão, só daquele restaurante
    db.execute(SQL_REFRESH_POLARIDADE, {"rid": restaurante_id})
    db.execute(SQL_REFRESH_GENERO, {"rid": restaurante_id})
    db.commit()

from sqlalchemy import func

def get_media_mensal_por_restaurante(db, restaurante_id: int):
    ano_mes = func.to_char(OpiniaoTemporal.data_publicacao, 'YYYY-MM')

    return (
        db.query(
            ano_mes.label("ano_mes"),
            func.avg(OpiniaoTemporal.polaridade).label("media_polaridade"),
            func.count().label("total_opinioes"),
        )
        .filter(OpiniaoTemporal.restaurante_id == restaurante_id)
        .group_by(ano_mes)
        .order_by(ano_mes)
        .all()
    )


from sqlalchemy import func, case
from models import OpiniaoTemporal

def get_opinioes_por_mes(db, restaurante_id: int):
    ano_mes = func.to_char(OpiniaoTemporal.data_publicacao, 'YYYY-MM')

    return (
        db.query(
            ano_mes.label("ano_mes"),
            func.sum(case((OpiniaoTemporal.polaridade >= 0.5, 1), else_=0)).label("positivas"),
            func.sum(case((OpiniaoTemporal.polaridade < 0.5, 1), else_=0)).label("negativas"),
        )
        .filter(OpiniaoTemporal.restaurante_id == restaurante_id)
        .group_by(ano_mes)
        .order_by(ano_mes)
        .all()
    )

