# CORRECTIONS.md — medlocalgpt

Base: knowledge-ukraine/medlocalgpt@14efc95 (master). Usuário autorizou implementação de todas as propostas viáveis.

## Implementado

1. **`.gitignore`** — ignora `medlocalgpt.env` e `SOURCE_DOCUMENTS/` (mantém `.gitkeep`). `constitution.pdf` já trackeado permanece.
2. **`.env.example`** (novo) — placeholders sem chaves reais; instrui a copiar para `medlocalgpt.env`.
3. **`SOURCE_DOCUMENTS/.gitkeep`** (novo) — mantém diretório vazio trackeado.
4. **`model_property.py`** — `MAX_TOKENS_OPENAI` lê `MAX_TOKENS_OPENAI`; `MAX_TOKENS_FOR_TRANSLATION` lê `MAX_TOKENS_FOR_TRANSLATION`; `INGEST_THREADS = os.cpu_count() or 1`.
5. **`ingest.py`** — guarda `SOURCE_DOCUMENTS` vazio (evita `range(0,0,0)` crash); `chunksize` mínimo 1.
6. **`stream_server.py`** — `debug=True` → `debug=False`.
7. **`run_server.py`** — `os.environ["no_proxy"] = "*"` comentado; typo `breast canser` → `breast cancer` (env + prompt UK).

## Não implementado (requer validação numérica/regressão com dependências)
- REA-005: inicialização do Chroma no nível do módulo.
- REA-006: validação de credenciais OpenAI.
- REA-007: remover `verbose=True` (logs com dados de saúde potenciais).
- REA-008: pins de duckdb/pandas/pyarrow + smoke test de ingest.
- REA-013: limitar workers do ThreadPoolExecutor.
- REA-015: autenticação/rate-limit nos endpoints de API.

## Validação
- `python -m py_compile` OK em todos os módulos modificados.
- Não executado: ingest/server (dependências ausentes).
