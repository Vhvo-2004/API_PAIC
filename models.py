from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Restaurante(Base):
    __tablename__ = "restaurante"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(200))
    categoria = Column(String(50))
    url_platform = Column(String(200))

    avaliacoes = relationship("Avaliacao", back_populates="restaurante")


class Avaliacao(Base):
    __tablename__ = "avaliacao"
    id = Column(Integer, primary_key=True, index=True)
    restaurante_id = Column(Integer, ForeignKey("restaurante.id"), nullable=False)
    usuario = Column(String(100))
    comentario = Column(Text, nullable=False)
    nota = Column(Integer)
    data = Column(DateTime)

    restaurante = relationship("Restaurante", back_populates="avaliacoes")
    aspectos = relationship("AvaliacaoAspecto", back_populates="avaliacao")


class Aspecto(Base):
    __tablename__ = "aspecto"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)

    avaliacao_aspecto = relationship("AvaliacaoAspecto", back_populates="aspecto")


class AvaliacaoAspecto(Base):
    __tablename__ = "avaliacao_aspecto"
    id = Column(Integer, primary_key=True, index=True)
    avaliacao_id = Column(Integer, ForeignKey("avaliacao.id"), nullable=False)
    aspecto_id = Column(Integer, ForeignKey("aspecto.id"), nullable=False)
    sentimento = Column(String(10))
    polaridade = Column(Float)
    nota_predita = Column(Integer)

    avaliacao = relationship("Avaliacao", back_populates="aspectos")
    aspecto = relationship("Aspecto", back_populates="avaliacao_aspecto")
