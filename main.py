from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import SessionLocal, engine
import uvicorn

# Cria as tabelas conforme os models novos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API - Sumarização de Avaliações de Restaurantes")

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

# >>> ROTA CORRIGIDA: comentários de um restaurante com 'autor' plano (compatível com MySQL/MariaDB)
@app.get("/comentarios/restaurante/{restaurante_id}", response_model=List[schemas.ComentarioOut])
def read_comentarios_por_restaurante(restaurante_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.Comentario,
            models.Cliente.nome.label("autor")
        )
        # outerjoin para não quebrar se o cliente tiver sido removido
        .outerjoin(models.Cliente, models.Cliente.id == models.Comentario.cliente_id)
        .filter(models.Comentario.restaurante_id == restaurante_id)
        # MariaDB/MySQL não suporta "NULLS LAST":
        # 1º ordena por "é nulo?" (False=0, True=1) => nulos por último
        # 2º dentro dos não-nulos, ordena por data desc
        .order_by(
            models.Comentario.data_publicacao.is_(None).asc(),
            models.Comentario.data_publicacao.desc()
        )
        .all()
    )

    return [
        schemas.ComentarioOut(
            id=c.id,
            data_publicacao=c.data_publicacao,
            curtidas=c.curtidas or 0,
            texto=c.texto,
            titulo=c.titulo,
            url=c.url,
            restaurante_id=c.restaurante_id,
            cliente_id=c.cliente_id,
            autor=(autor or "Desconhecido")
        )
        for (c, autor) in rows
    ]

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
    
from fastapi import Query
# ----- Charts: leituras -----
@app.get("/charts/polaridade/{restaurante_id}", response_model=List[schemas.ChartPolaridadeAspecto])
def chart_polaridade(restaurante_id: int, aspecto: str | None = Query(None), db: Session = Depends(get_db)):
    return crud.get_chart_polaridade(db, restaurante_id, aspecto)

@app.get("/charts/genero/{restaurante_id}", response_model=List[schemas.ChartGeneroAspecto])
def chart_genero(restaurante_id: int, categoria_id: int | None = Query(None), db: Session = Depends(get_db)):
    return crud.get_chart_genero(db, restaurante_id, categoria_id)

# ----- Chart: Polaridade por Categoria -----
@app.get("/charts/polaridade-categoria/{restaurante_id}", response_model=List[schemas.ChartPolaridadeCategoria])
def chart_polaridade_categoria(restaurante_id: int, db: Session = Depends(get_db)):
    """
    Retorna as médias de polaridade e quantidade de opiniões
    por categoria para um restaurante específico.
    """
    rows = (
        db.query(models.ChartPolaridadeCategoria)
        .filter(models.ChartPolaridadeCategoria.restaurante_id == restaurante_id)
        .order_by(models.ChartPolaridadeCategoria.categoria_nome.asc())
        .all()
    )
    return rows


@app.get("/graficos/media-mensal/{restaurante_id}")
def grafico_media_mensal(restaurante_id: int, db: Session = Depends(get_db)):
    dados = crud.get_media_mensal_por_restaurante(db, restaurante_id)
    return [
        {"ano_mes": r[0], "media_polaridade": float(r[1]), "total_opinioes": r[2]}
        for r in dados
    ]
@app.get("/graficos/temporal/{restaurante_id}")
def grafico_temporal(restaurante_id: int, db: Session = Depends(get_db)):
    dados = crud.get_opinioes_por_mes(db, restaurante_id)
    return [
        {
            "ano_mes": r[0],
            "positivas": int(r[1]),
            "negativas": int(r[2])
        }
        for r in dados
    ]
# --------- ENTRYPOINT PARA O RENDER ---------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )