# SIAR - Etapa de atualização das tabelas do aplicativo

Este ajuste implementa **somente** a etapa de sincronização das tabelas agregadas consumidas pelo app Android, usando dados das tabelas primárias.

## Origem (primárias)
- `comentario`
- `opiniao`
- `categoria_opiniao`

## Destino (consultadas pelo app)
- `chart_polaridade_aspecto`
- `chart_polaridade_categoria`
- `chart_polaridade_categoria_temporal`
- `opinioes_temporal`
- `media_mensal`

## Arquivos
- SQL da atualização: `pipeline/sql/refresh_aggregates.sql`
- Serviço Python: `pipeline/services/aggregation_service.py`
- Script executável: `scripts/run_refresh_app_tables.py`

## Como executar (script)
```bash
./scripts/run_refresh_app_tables.py
./scripts/run_refresh_app_tables.py --restaurante-id 1
```

## Como executar (Python)
```python
from database import SessionLocal
from pipeline.services.aggregation_service import refresh_app_tables

with SessionLocal() as db:
    refresh_app_tables(db)              # todos os restaurantes
    # refresh_app_tables(db, 1)         # apenas restaurante_id=1
```

## Observação
A query usa parâmetro `:rid` para permitir atualização global ou por restaurante.


## Polaridade temporal por categoria
A tabela `chart_polaridade_categoria_temporal` guarda uma linha por restaurante, categoria e mês (`periodo` no primeiro dia do mês), com `qt_opinioes` e `avg_polaridade`.

Ela alimenta os endpoints:
- `GET /charts/polaridade-categoria-temporal/{restaurante_id}`
- `GET /graficos/histograma-categoria/{restaurante_id}`

Ambos aceitam o filtro opcional `categoria_id` para retornar apenas uma categoria no histograma temporal.
