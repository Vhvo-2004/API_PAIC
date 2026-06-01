/*
Etapa única de atualização das tabelas consultadas no app.
Filtro opcional:
  :rid = NULL  -> atualiza todos os restaurantes
  :rid = <id>  -> atualiza apenas 1 restaurante
*/


CREATE TABLE IF NOT EXISTS chart_polaridade_categoria_temporal (
    restaurante_id BIGINT NOT NULL,
    categoria_id BIGINT NOT NULL,
    categoria_nome VARCHAR(255),
    periodo DATE NOT NULL,
    qt_opinioes INTEGER NOT NULL,
    avg_polaridade DOUBLE PRECISION NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (restaurante_id, categoria_id, periodo)
);

-- 1) chart_polaridade_aspecto
INSERT INTO chart_polaridade_aspecto (restaurante_id, aspecto, avg_polaridade, qt_opinioes, updated_at)
SELECT
    c.restaurante_id,
    o.aspecto,
    AVG(o.polaridade) AS avg_polaridade,
    COUNT(*) AS qt_opinioes,
    NOW() AS updated_at
FROM opiniao o
JOIN comentario c ON c.id = o.comentario_id
WHERE (:rid IS NULL OR c.restaurante_id = :rid)
GROUP BY c.restaurante_id, o.aspecto
ON CONFLICT (restaurante_id, aspecto)
DO UPDATE SET
    avg_polaridade = EXCLUDED.avg_polaridade,
    qt_opinioes = EXCLUDED.qt_opinioes,
    updated_at = NOW();

-- 2) chart_polaridade_categoria
INSERT INTO chart_polaridade_categoria (restaurante_id, categoria_id, categoria_nome, qt_opinioes, avg_polaridade, updated_at)
SELECT
    c.restaurante_id,
    co.id AS categoria_id,
    co.categoria AS categoria_nome,
    COUNT(*) AS qt_opinioes,
    AVG(o.polaridade) AS avg_polaridade,
    NOW() AS updated_at
FROM opiniao o
JOIN comentario c ON c.id = o.comentario_id
JOIN categoria_opiniao co ON co.id = o.categoria_id
WHERE (:rid IS NULL OR c.restaurante_id = :rid)
GROUP BY c.restaurante_id, co.id, co.categoria
ON CONFLICT (restaurante_id, categoria_id, categoria_nome)
DO UPDATE SET
    qt_opinioes = EXCLUDED.qt_opinioes,
    avg_polaridade = EXCLUDED.avg_polaridade,
    updated_at = NOW();


-- 3) chart_polaridade_categoria_temporal
DELETE FROM chart_polaridade_categoria_temporal cpct
WHERE (:rid IS NULL OR cpct.restaurante_id = :rid);

INSERT INTO chart_polaridade_categoria_temporal (
    restaurante_id, categoria_id, categoria_nome, periodo, qt_opinioes, avg_polaridade, updated_at
)
SELECT
    c.restaurante_id,
    co.id AS categoria_id,
    co.categoria AS categoria_nome,
    date_trunc('month', c.data_publicacao)::date AS periodo,
    COUNT(*) AS qt_opinioes,
    AVG(o.polaridade) AS avg_polaridade,
    NOW() AS updated_at
FROM opiniao o
JOIN comentario c ON c.id = o.comentario_id
JOIN categoria_opiniao co ON co.id = o.categoria_id
WHERE c.data_publicacao IS NOT NULL
  AND (:rid IS NULL OR c.restaurante_id = :rid)
GROUP BY c.restaurante_id, co.id, co.categoria, date_trunc('month', c.data_publicacao)::date;

-- 4) opinioes_temporal (reconstrução incremental por restaurante)
DELETE FROM opinioes_temporal ot
USING comentario c
WHERE ot.comentario_id = c.id
  AND (:rid IS NULL OR c.restaurante_id = :rid);

INSERT INTO opinioes_temporal (
    opiniao_id, comentario_id, restaurante_id, cliente_id,
    aspecto, polaridade, sentimento, sentenca, categoria_id, data_publicacao
)
SELECT
    o.id,
    c.id,
    c.restaurante_id,
    c.cliente_id,
    o.aspecto,
    o.polaridade,
    o.sentimento,
    o.sentenca,
    o.categoria_id,
    c.data_publicacao
FROM opiniao o
JOIN comentario c ON c.id = o.comentario_id
WHERE (:rid IS NULL OR c.restaurante_id = :rid);

-- 5) media_mensal
DELETE FROM media_mensal mm
WHERE (:rid IS NULL OR mm.restaurante_id = :rid);

INSERT INTO media_mensal (restaurante_id, ano_mes, media_polaridade, total_opinioes, updated_at)
SELECT
    c.restaurante_id,
    to_char(c.data_publicacao, 'YYYY-MM') AS ano_mes,
    AVG(o.polaridade) AS media_polaridade,
    COUNT(*) AS total_opinioes,
    NOW() AS updated_at
FROM opiniao o
JOIN comentario c ON c.id = o.comentario_id
WHERE c.data_publicacao IS NOT NULL
  AND (:rid IS NULL OR c.restaurante_id = :rid)
GROUP BY c.restaurante_id, to_char(c.data_publicacao, 'YYYY-MM');
