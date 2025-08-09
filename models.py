from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Restaurante(Base):
    __tablename__ = "restaurante"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)

    comentarios = relationship("Comentario", back_populates="restaurante", cascade="all, delete-orphan")


class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150))
    login = Column(String(60))
    genero = Column(String(20))

    comentarios = relationship("Comentario", back_populates="cliente", cascade="all, delete-orphan")


class Comentario(Base):
    __tablename__ = "comentario"
    id = Column(Integer, primary_key=True, index=True)
    data_publicacao = Column(DateTime)
    curtidas = Column(Integer)
    texto = Column(Text, nullable=False)
    titulo = Column(String(200))
    url = Column(String(300))

    restaurante_id = Column(Integer, ForeignKey("restaurante.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    restaurante = relationship("Restaurante", back_populates="comentarios")
    cliente = relationship("Cliente", back_populates="comentarios")
    opinioes = relationship("Opiniao", back_populates="comentario", cascade="all, delete-orphan")


class CategoriaOpiniao(Base):
    __tablename__ = "categoria_opiniao"
    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(100), nullable=False)

    opinioes = relationship("Opiniao", back_populates="categoria")


class Opiniao(Base):
    __tablename__ = "opiniao"
    id = Column(Integer, primary_key=True, index=True)
    aspecto = Column(String(100), nullable=False)     # ex.: "comida", "atendimento", etc.
    sentimento = Column(String(50))                   # ex.: "positivo", "negativo", "neutro"
    polaridade = Column(Float)                        # ex.: -1.0 a 1.0 ou 0..1
    sentenca = Column(Text)                           # trecho de texto/justificativa

    comentario_id = Column(Integer, ForeignKey("comentario.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria_opiniao.id"), nullable=True)

    comentario = relationship("Comentario", back_populates="opinioes")
    categoria = relationship("CategoriaOpiniao", back_populates="opinioes")
