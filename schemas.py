from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RestauranteBase(BaseModel):
    nome: str
    endereco: Optional[str]
    categoria: Optional[str]
    url_platform: Optional[str]

class RestauranteCreate(RestauranteBase):
    pass

class Restaurante(RestauranteBase):
    id: int
    class Config:
        orm_mode = True


class AvaliacaoBase(BaseModel):
    restaurante_id: int
    usuario: Optional[str]
    comentario: str
    nota: Optional[int]
    data: Optional[datetime]

class AvaliacaoCreate(AvaliacaoBase):
    pass

class Avaliacao(AvaliacaoBase):
    id: int
    class Config:
        orm_mode = True


class AspectoBase(BaseModel):
    nome: str

class AspectoCreate(AspectoBase):
    pass

class Aspecto(AspectoBase):
    id: int
    class Config:
        orm_mode = True


class AvaliacaoAspectoBase(BaseModel):
    avaliacao_id: int
    aspecto_id: int
    sentimento: Optional[str]
    polaridade: Optional[float]
    nota_predita: Optional[int]

class AvaliacaoAspectoCreate(AvaliacaoAspectoBase):
    pass

class AvaliacaoAspecto(AvaliacaoAspectoBase):
    id: int
    class Config:
        orm_mode = True
