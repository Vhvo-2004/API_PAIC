# populate_mock.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from faker import Faker
from datetime import timedelta
import random

import models  # nova estrutura (Restaurante, Cliente, Comentario, Opiniao, CategoriaOpiniao)
from database import SessionLocal

fake = Faker("pt_BR")
random.seed(42)
Faker.seed(42)

db: Session = SessionLocal()

# ---------- Helpers ----------
def sentimento_por_polaridade(p):
    if p is None:
        return random.choice(["positivo", "neutro", "negativo"])
    if p > 0.15:
        return "positivo"
    elif p < -0.15:
        return "negativo"
    return "neutro"

# ---------- Limpeza segura ----------
def limpar_banco(db: Session, drop_tabelas_antigas: bool = True):
    """
    Limpa as tabelas da nova estrutura e, opcionalmente, remove as TABELAS ANTIGAS
    (avaliacao, aspecto, avaliacao_aspecto) que causam o erro 1451.
    """
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))

    # --- Dropa TABELAS ANTIGAS se existirem (do schema anterior) ---
    if drop_tabelas_antigas:
        db.execute(text("DROP TABLE IF EXISTS avaliacao_aspecto"))
        db.execute(text("DROP TABLE IF EXISTS avaliacao"))
        db.execute(text("DROP TABLE IF EXISTS aspecto"))

    # --- Limpa TABELAS NOVAS na ordem correta ---
    # Opiniao -> Comentario -> Cliente/Restaurante -> CategoriaOpiniao
    db.execute(text("DELETE FROM opiniao"))
    db.execute(text("DELETE FROM comentario"))
    db.execute(text("DELETE FROM cliente"))
    db.execute(text("DELETE FROM restaurante"))
    db.execute(text("DELETE FROM categoria_opiniao"))

    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    db.commit()

# ---------- Populador ----------
def popular_banco(
    num_restaurantes: int = 5,
    num_clientes: int = 20,
    comentarios_por_rest_min: int = 8,
    comentarios_por_rest_max: int = 14,
    opinioes_por_coment_min: int = 1,
    opinioes_por_coment_max: int = 4,
    aspectos_base=None,
    categorias_base=None,
):
    if aspectos_base is None:
        aspectos_base = ["comida", "atendimento", "preço", "ambiente"]
    if categorias_base is None:
        categorias_base = ["Sabor", "Serviço", "Custo-Benefício", "Ambiente"]

    limpar_banco(db, drop_tabelas_antigas=True)

    # Categorias
    cat_objs = []
    for nome in categorias_base:
        c = models.CategoriaOpiniao(categoria=nome)
        db.add(c)
        cat_objs.append(c)
    db.commit()

    # Clientes
    clientes = []
    for _ in range(num_clientes):
        cli = models.Cliente(
            nome=fake.name(),
            email=fake.unique.email(),
            login=fake.user_name(),
            genero=random.choice(["masculino", "feminino", "outro"]),
        )
        db.add(cli)
        clientes.append(cli)
    db.commit()

    # Restaurantes
    restaurantes = []
    for _ in range(num_restaurantes):
        r = models.Restaurante(
            nome=fake.company(),
        )
        db.add(r)
        restaurantes.append(r)
    db.commit()

    # Comentários + Opiniões (1:N)
    for rest in restaurantes:
        qtd_coment = random.randint(comentarios_por_rest_min, comentarios_por_rest_max)
        for _ in range(qtd_coment):
            cliente = random.choice(clientes)
            dt = fake.date_time_this_year() - timedelta(days=random.randint(0, 120))

            comentario = models.Comentario(
                data_publicacao=dt,
                curtidas=random.randint(0, 500),
                texto=fake.paragraph(nb_sentences=random.randint(1, 3)),
                titulo=fake.sentence(nb_words=6),
                url=fake.url(),
                restaurante_id=rest.id,
                cliente_id=cliente.id,
            )
            db.add(comentario)
            db.commit()  # precisa do ID para FK

            qtd_opinioes = random.randint(opinioes_por_coment_min, opinioes_por_coment_max)
            aspectos_escolhidos = random.sample(
                aspectos_base,
                k=min(qtd_opinioes, len(aspectos_base))
            )
            for asp in aspectos_escolhidos:
                pol = round(random.uniform(-1, 1), 2)
                opiniao = models.Opiniao(
                    aspecto=asp,
                    sentimento=sentimento_por_polaridade(pol),
                    polaridade=pol,
                    sentenca=fake.sentence(nb_words=random.randint(6, 16)),
                    comentario_id=comentario.id,
                    categoria_id=random.choice(cat_objs).id if random.random() < 0.9 else None,
                )
                db.add(opiniao)
        db.commit()

    print("✅ Banco populado com sucesso!")

if __name__ == "__main__":
    popular_banco()
