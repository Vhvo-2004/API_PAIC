#!/usr/bin/env python3
from __future__ import annotations

import argparse

from database import SessionLocal
from pipeline.services.aggregation_service import refresh_app_tables


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Atualiza as tabelas agregadas consultadas pelo app Android."
    )
    parser.add_argument(
        "--restaurante-id",
        type=int,
        default=None,
        help="Atualiza apenas um restaurante específico. Se omitido, atualiza todos.",
    )
    args = parser.parse_args()

    with SessionLocal() as db:
        refresh_app_tables(db, restaurante_id=args.restaurante_id)

    alvo = f"restaurante_id={args.restaurante_id}" if args.restaurante_id is not None else "todos os restaurantes"
    print(f"Refresh concluído para {alvo}.")


if __name__ == "__main__":
    main()
