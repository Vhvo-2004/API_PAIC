from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ---- Restaurante ----
class RestauranteBase(BaseModel):
    nome: str

class RestauranteCreate(RestauranteBase):
    pass

class Restaurante(RestauranteBase):
    id: int
    class Config:
        orm_mode = True


# ---- Cliente ----
class ClienteBase(BaseModel):
    nome: str
    email: Optional[str] = None
    login: Optional[str] = None
    genero: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    class Config:
        orm_mode = True


# ---- Comentario ----
class ComentarioBase(BaseModel):
    data_publicacao: Optional[datetime] = None
    curtidas: Optional[int] = None
    texto: str
    titulo: Optional[str] = None
    url: Optional[str] = None
    restaurante_id: int
    cliente_id: int

class ComentarioCreate(ComentarioBase):
    pass

class Comentario(ComentarioBase):
    id: int
    class Config:
        orm_mode = True

# >>> Opção A: payload de saída com o autor plano <<<
class ComentarioOut(BaseModel):
    id: int
    data_publicacao: Optional[datetime] = None
    curtidas: int
    texto: str
    titulo: Optional[str] = None
    url: Optional[str] = None
    restaurante_id: int
    cliente_id: int
    autor: Optional[str] = None

    class Config:
        orm_mode = True


# ---- Categoria de Opinião ----
class CategoriaOpiniaoBase(BaseModel):
    categoria: str

class CategoriaOpiniaoCreate(CategoriaOpiniaoBase):
    pass

class CategoriaOpiniao(CategoriaOpiniaoBase):
    id: int
    class Config:
        orm_mode = True


# ---- Opinião ----
class OpiniaoBase(BaseModel):
    aspecto: str
    sentimento: Optional[str] = None
    polaridade: Optional[float] = None
    sentenca: Optional[str] = None
    comentario_id: int
    categoria_id: Optional[int] = None

class OpiniaoCreate(OpiniaoBase):
    pass

class Opiniao(OpiniaoBase):
    id: int
    class Config:
        orm_mode = True


# ---- Comparação (mantido para compatibilidade com sua UI) ----
class AspectoComparado(BaseModel):
    aspecto: str
    notaPredita1: Decimal
    notaPredita2: Decimal
