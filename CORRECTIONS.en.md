# CORRECTIONS.md — medlocalgpt

Base: knowledge-ukraine/medlocalgpt@14efc95 (master). User authorized implementation of all viable proposals.

## Implemented

1. **`.gitignore`** — ignores `medlocalgpt.env` and `SOURCE_DOCUMENTS/` (keeps `.gitkeep`). `constitution.pdf` already tracked remains.
2. **`.env.example`** (new) — placeholders without real keys; instructs to copy to `medlocalgpt.env`.
3. **`SOURCE_DOCUMENTS/.gitkeep`** (new) — keeps empty directory tracked.
4. **`model_property.py`** — `MAX_TOKENS_OPENAI` reads `MAX_TOKENS_OPENAI`; `MAX_TOKENS_FOR_TRANSLATION` reads `MAX_TOKENS_FOR_TRANSLATION`; `INGEST_THREADS = os.cpu_count() or 1`.
5. **`ingest.py`** — guards empty `SOURCE_DOCUMENTS` (avoids `range(0,0,0)` crash); `chunksize` minimum 1.
6. **`stream_server.py`** — `debug=True` → `debug=False`.
7. **`run_server.py`** — `os.environ["no_proxy"] = "*"` commented out; typo `breast canser` → `breast cancer` (env + UK prompt).

## Not implemented (requires numeric validation/regression with dependencies)
- REA-005: Chroma initialization at module level.
- REA-006: OpenAI credential validation.
- REA-007: remove `verbose=True` (logs with potential health data).
- REA-008: duckdb/pandas/pyarrow pins + ingest smoke test.
- REA-013: limit ThreadPoolExecutor workers.
- REA-015: authentication/rate-limit on API endpoints.

## Validation
- `python -m py_compile` OK on all modified modules.
- Not executed: ingest/server (missing dependencies).
