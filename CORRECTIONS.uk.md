# CORRECTIONS.md — medlocalgpt

База: knowledge-ukraine/medlocalgpt@14efc95 (master). Користувач авторизував впровадження всіх життєздатних пропозицій.

## Впроваджено

1. **`.gitignore`** — ігнорує `medlocalgpt.env` і `SOURCE_DOCUMENTS/` (зберігає `.gitkeep`). `constitution.pdf` вже відслідковується залишається.
2. **`.env.example`** (новий) — мітки заміщення без реальних ключів; інструкція скопіювати до `medlocalgpt.env`.
3. **`SOURCE_DOCUMENTS/.gitkeep`** (новий) — зберігає порожній каталог відслідковуваним.
4. **`model_property.py`** — `MAX_TOKENS_OPENAI` читає `MAX_TOKENS_OPENAI`; `MAX_TOKENS_FOR_TRANSLATION` читає `MAX_TOKENS_FOR_TRANSLATION`; `INGEST_THREADS = os.cpu_count() or 1`.
5. **`ingest.py`** — захист від порожнього `SOURCE_DOCUMENTS` (уникнення падіння `range(0,0,0)`); `chunksize` мінімум 1.
6. **`stream_server.py`** — `debug=True` → `debug=False`.
7. **`run_server.py`** — `os.environ["no_proxy"] = "*"` закоментовано; помилка написання `breast canser` → `breast cancer` (env + український запит).

## Не впроваджено (потребує числової валідації/регресії з залежностями)
- REA-005: ініціалізація Chroma на рівні модуля.
- REA-006: перевірка облікових даних OpenAI.
- REA-007: видалити `verbose=True` (логи з потенційними даними про здоров'я).
- REA-008: закріплення версій duckdb/pandas/pyarrow + smoke test ingest.
- REA-013: обмеження працівників ThreadPoolExecutor.
- REA-015: автентифікація/обмеження швидкості на API кінцевих точках.

## Валідація
- `python -m py_compile` OK на всіх модифікованих модулях.
- Не виконано: ingest/server (відсутні залежності).
