# Guia para consumo da API por um site web

A API já possui endpoints de gráficos que podem ser consumidos pelo site. Para o navegador permitir chamadas vindas de outro domínio/porta, a API habilita CORS usando a variável de ambiente `ALLOWED_ORIGINS`.

## Configuração de CORS

Defina `ALLOWED_ORIGINS` com uma lista separada por vírgulas contendo as origens autorizadas do site:

```bash
ALLOWED_ORIGINS="https://seu-site.com,https://www.seu-site.com"
```

Para desenvolvimento local, a API libera por padrão:

- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

Evite usar `*` em produção. Prefira informar explicitamente os domínios do site.

## Endpoints úteis para gráficos

- `GET /charts/polaridade/{restaurante_id}`
- `GET /charts/genero/{restaurante_id}`
- `GET /charts/polaridade-categoria/{restaurante_id}`
- `GET /charts/polaridade-categoria-temporal/{restaurante_id}`
- `GET /graficos/histograma-categoria/{restaurante_id}`
- `GET /graficos/media-mensal/{restaurante_id}`
- `GET /graficos/temporal/{restaurante_id}`

## Exemplo de consumo no front-end

```javascript
const apiUrl = import.meta.env.VITE_API_URL;
const restauranteId = 1;

const response = await fetch(`${apiUrl}/charts/polaridade-categoria/${restauranteId}`);
const dados = await response.json();
```

O site deve chamar a API HTTP; ele não deve acessar o banco de dados diretamente.
