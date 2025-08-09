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


def comparar_aspectos(db, restaurante1_id: int, restaurante2_id: int):
    """
    Calcula a média de polaridade por 'aspecto' para dois restaurantes
    em uma única query usando agregação condicional (CASE).
    Inclui aspectos presentes em pelo menos um dos dois restaurantes.
    """
    rows = (
        db.query(
            models.Opiniao.aspecto.label("aspecto"),
            func.avg(
                case(
                    (models.Comentario.restaurante_id == restaurante1_id, models.Opiniao.polaridade),
                    else_=None,
                )
            ).label("nota_predita1"),
            func.avg(
                case(
                    (models.Comentario.restaurante_id == restaurante2_id, models.Opiniao.polaridade),
                    else_=None,
                )
            ).label("nota_predita2"),
        )
        .join(models.Comentario, models.Opiniao.comentario_id == models.Comentario.id)
        .filter(models.Comentario.restaurante_id.in_([restaurante1_id, restaurante2_id]))
        .group_by(models.Opiniao.aspecto)
        .all()
    )

    out = []
    for r in rows:
        n1 = round(float(r.nota_predita1) if r.nota_predita1 is not None else 0.0, 3)
        n2 = round(float(r.nota_predita2) if r.nota_predita2 is not None else 0.0, 3)
        out.append({"aspecto": r.aspecto, "notaPredita1": n1, "notaPredita2": n2})
    # ordenar opcionalmente por aspecto
    out.sort(key=lambda x: x["aspecto"] or "")
    return out