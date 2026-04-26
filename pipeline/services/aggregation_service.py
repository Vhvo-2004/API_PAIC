from __future__ import annotations

from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

SQL_FILE = Path(__file__).resolve().parent.parent / "sql" / "refresh_aggregates.sql"


def refresh_app_tables(db: Session, restaurante_id: int | None = None) -> None:
    """
    Atualiza tabelas consultadas pelo app Android a partir das tabelas primárias.

    Tabelas primárias fonte:
      - comentario
      - opiniao
      - categoria_opiniao

    Tabelas de consulta destino:
      - chart_polaridade_aspecto
      - chart_polaridade_categoria
      - opinioes_temporal
      - media_mensal
    """
    db.execute(text(SQL_FILE.read_text(encoding="utf-8")), {"rid": restaurante_id})
    db.commit()
