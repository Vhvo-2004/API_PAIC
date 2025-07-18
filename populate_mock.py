from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime
import random

# Cria todas as tabelas no banco (caso não existam)
models.Base.metadata.create_all(bind=engine)

# Abre sessão com o banco
db: Session = SessionLocal()

# 🔥 RESET: limpa todas as tabelas para garantir integridade
print("🧹 Limpando todas as tabelas (Avaliacoes, AvaliacaoAspecto, Restaurante, Aspecto)...")
db.query(models.AvaliacaoAspecto).delete()
db.query(models.Avaliacao).delete()
db.query(models.Restaurante).delete()
db.query(models.Aspecto).delete()
db.commit()

# 1. Inserindo restaurantes mock
restaurantes_mock = [
    models.Restaurante(nome="Pizzaria Saborosa", endereco="Rua A, 123", categoria="Pizza", url_platform="https://pizzariasaborosa.com"),
    models.Restaurante(nome="Sushi Place", endereco="Av B, 456", categoria="Sushi", url_platform="https://sushiplace.com"),
    models.Restaurante(nome="Churrascaria Fogo Alto", endereco="Rua C, 789", categoria="Churrasco", url_platform="https://fogoalto.com"),
]

db.add_all(restaurantes_mock)
db.commit()

# 🔄 Recarrega os restaurantes do banco para garantir IDs corretos
restaurantes_mock = db.query(models.Restaurante).all()

# 2. Inserindo aspectos mock
aspectos_mock = ["atendimento", "preço", "qualidade", "tempo de entrega"]

aspecto_objs = []
for asp in aspectos_mock:
    aspecto = models.Aspecto(nome=asp)
    db.add(aspecto)
    db.commit()
    aspecto_objs.append(aspecto)

# 3. Inserindo avaliações mock para cada restaurante
for rest in restaurantes_mock:
    for i in range(20):  # 🔥 20 avaliações por restaurante
        avaliacao = models.Avaliacao(
            restaurante_id=rest.id,
            usuario=f"Usuario{i}",
            comentario=f"Comentário exemplo {i} para {rest.nome}",
            nota=random.randint(1, 5),
            data=datetime.now()
        )
        db.add(avaliacao)
        db.commit()

        # 4. Inserindo aspectos nas avaliações
        for aspecto in aspecto_objs:
            avaliacao_aspecto = models.AvaliacaoAspecto(
                avaliacao_id=avaliacao.id,
                aspecto_id=aspecto.id,
                sentimento=random.choice(["positivo", "negativo", "neutro"]),
                polaridade=round(random.uniform(-1, 1), 2),
                nota_predita=random.randint(1, 5)
            )
            db.add(avaliacao_aspecto)
        db.commit()

db.close()
print("✅ Banco resetado COMPLETAMENTE e populado com dados mock para teste.")
