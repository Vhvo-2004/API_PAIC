# SIAR - Etapa de atualização das tabelas do aplicativo

Este ajuste implementa **somente** a etapa de sincronização das tabelas agregadas consumidas pelo app Android, usando dados das tabelas primárias.

## Origem (primárias)
- `comentario`
- `opiniao`
- `categoria_opiniao`

## Destino (consultadas pelo app)
- `chart_polaridade_aspecto`
- `chart_polaridade_categoria`
- `opinioes_temporal`
- `media_mensal`

## Arquivos
- SQL da atualização: `pipeline/sql/refresh_aggregates.sql`
- Serviço Python: `pipeline/services/aggregation_service.py`

## Como executar
```python
from database import SessionLocal
from pipeline.services.aggregation_service import refresh_app_tables

with SessionLocal() as db:
    refresh_app_tables(db)              # todos os restaurantes
    # refresh_app_tables(db, 1)         # apenas restaurante_id=1
```

## Observação
A query usa parâmetro `:rid` para permitir atualização global ou por restaurante.
