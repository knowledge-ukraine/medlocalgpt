# ЗВІТ З РЕВЕРСНОЇ ІНЖЕНЕРІЇ — knowledge-ukraine/medlocalgpt

## Оригінальний репозиторій
- Назва: medlocalgpt
- URL: https://github.com/knowledge-ukraine/medlocalgpt
- Тип: Асистент RAG на основі LLM для фізичної реабілітації та телереабілітації (Flask + LangChain + Chroma)
- Гілка: master
- База: 14efc95 docs: update project funding details (#23)

## Дата аудиту
2026-11-07

## Використані інструменти
- Git v2.49.0
- PowerShell 5.1
- gh (GitHub CLI), автентифіковано як admeduardovieira
- Kilo Code (статичний аналіз файлів Python/YAML)
- python 3.12.14 (тільки py_compile — синтаксис)

## Виявлена архітектура
Додаток Flask з конвеєром RAG (Retrieval-Augmented Generation) над даними про реабілітацію (EBSCO).
Компоненти:
- run_server.py: Flask API, ланцюжки LangChain (OpenAI/локально), пошуковик Chroma, маршрути /medlocalgpt/api/v1/*/ask
- ingest.py: завантажує SOURCE_DOCUMENTS, виконує chunking (RecursiveCharacterTextSplitter), вбудування за допомогою HuggingFaceInstructEmbeddings, зберігає Chroma (duckdb+parquet)
- model_property.py: конфігурація через змінні середовища (medlocalgpt.env)
- stream_server.py: приклад потокового передавання LangChain (debug=True)
- wsgi.py / deploy/uwsgi.ini / docker-compose.yml / deploy/nginx.conf: продакшн
- Інтерфейс: templates/index.html + static/ (JS/CSS)

## Технології та залежності
Python 3.10, Flask, LangChain 0.0.191, Chroma 0.3.22 (duckdb+parquet), OpenAI SDK, googletrans, sentence-transformers, llama-cpp-python, auto-gptq, uWSGI, nginx.
requirements.txt без достовірного закріплення версій; deploy/requirements.txt дублюється.

## Стан обслуговування
- 1 відкрите питання (#20, duckdb/pandas, 2023-09-04, все ще не вирішене)
- 23 PR (всі злито; #2 "Fixed exposed openai token" — свідчення про попереднє розкриття облікових даних)
- Остання функційна діяльність: 2023-09; документація: 2025-09
- Немає автоматизованих тестів, немає CI, немає pytest

## Обмеження дослідження
- Немає середовища Python з залежностями (langchain, chromadb, torch тощо) для запуску ingest/server/benchmarkів
- Це не проєкт FHIR/SUSHI (правила releaselabel не поширюються)

---

## Виявлені проблеми (medlocalgpt)

| ID | Sev | Статус | Місцезнаходження | Проблема | Виправлення застосовано |
|---|---|---|---|---|---|
| REA-001 | P0 | ПІДТВЕРДжено | medlocalgpt.env (відслідковується), .gitignore | Файл середовища з OPENAI_API_KEY/OPENAI_ORGANIZATION відслідковується; .gitignore ігнорує лише .env, а не medlocalgpt.env | .gitignore ігнорує medlocalgpt.env + SOURCE_DOCUMENTS/ (крім .gitkeep); .env.example з мітками заміщення |
| REA-002 | P1 | ПІДТВЕРДжено | model_property.py:44 | MAX_TOKENS_OPENAI читає os.environ['MAX_TOKENS'] (неправильна змінна) | Читає MAX_TOKENS_OPENAI |
| REA-003 | P1 | ПІДТВЕРДжено | model_property.py:49 | MAX_TOKENS_FOR_TRANSLATION читає os.environ['MAX_TOKENS'] (неправильна змінна) | Читає MAX_TOKENS_FOR_TRANSLATION |
| REA-004 | P1 | ПІДТВЕРДжено | ingest.py:58-63 | SOURCE_DOCUMENTS порожній → chunksize=0 → range(0,0,0) ValueError | Захист від порожніх шляхів; мінімальний chunksize 1 |
| REA-005 | P2 | ПІДТВЕРДжено | run_server.py:150-155 | EMBEDDINGS/DB (Chroma) створені на рівні модуля; помилка load_model блокує сервер | Не виправлено в цьомураунді (потребує регресії) |
| REA-006 | P2 | ПІДТВЕРДжено | run_server.py:167 | Заплутана перевірка облікових даних (is not None; не відхиляє порожні рядки) | Не виправлено в цьомураунді |
| REA-007 | P2 | Ймовірно | run_server.py:364 | SimpleSequentialChain verbose=True логує запити/відповіді (потенційні дані про здоров'я) | Не виправлено в цьомураунді |
| REA-008 | P2 | ПІДТВЕРДжено | requirements.txt / deploy/requirements.txt / Issue #20 | Несумісність duckdb/pandas/pyarrow; питання відкрите з 2023-09-04 | Не виправлено в цьомураунді (потребує закріплення версій + smoke test) |
| REA-009 | P3 | ПІДТВЕРДжено | medlocalgpt.env:6; run_server.py:329 | Помилка написання "breast canser" | Виправлено на "breast cancer" |
| REA-010 | P2 | ПІДТВЕРДжено | stream_server.py:94; run_server.py:4 | stream_server.py debug=True (відкриває трасування стека); run_server.py no_proxy="*" (обхід проксі/мережевого екрана) | debug=False; no_proxy закоментовано |
| REA-011 | P3 | ПІДТВЕРДжено | model_property.py:94 | INGEST_THREADS = os.cpu_count() може бути None → TypeError | За замовчуванням 1, якщо None |
| REA-012 | P3 | ПІДТВЕРДжено | requirements.txt | Залежності без достовірного закріплення версій; Streamlit-extras неправильна назва; InstructorEmbedding сумнівний | Не виправлено в цьомураунді |
| REA-013 | P3 | ПІДТВЕРДжено | ingest.py:37 | ThreadPoolExecutor(len(filepaths)) — необмежена кількість потоків | Не виправлено в цьомураунді |
| REA-014 | P3 | ПІДТВЕРДжено | .gitignore; SOURCE_DOCUMENTS/constitution.pdf | Каталог документів користувача не ігнорується; constitution.pdf (потенційна PHI) відслідковується | SOURCE_DOCUMENTS/ ігнорується (крім .gitkeep); constitution.pdf залишається відслідковуваним (вже версійований) |
| REA-015 | P3 | ГІПОТЕЗА | run_server.py маршрути | Відсутність автентифікації/обмеження швидкості на API кінцевих точках | Не виправлено в цьомураунді |

## Повторювані проблеми
1. Несумісність duckdb/pandas (Питання #20) — відкрито 2023-09-04, все ще не вирішено; коміти fix pandas не запобігли пропуску.
2. Розкриття облікових даних (PR #2) — вже відбулося; medlocalgpt.env все ще відслідковується (ризик залишається).

## Нездокументовані помилки (нові з аудиту)
REA-002, REA-003, REA-004, REA-005, REA-006, REA-009, REA-010, REA-011, REA-013, REA-014, REA-015 не мають публічного запису.

## Зміни, що було впроваджено (Фаза 2)
1. `.gitignore`: ігнорує medlocalgpt.env і SOURCE_DOCUMENTS/ (зберігає .gitkeep); constitution.pdf вже відслідковується залишається.
2. `.env.example` (новий): мітки заміщення без реальних ключів.
3. `SOURCE_DOCUMENTS/.gitkeep` (новий): зберігає порожній каталог відслідковуваним.
4. `model_property.py`: виправлення читання MAX_TOKENS_OPENAI / MAX_TOKENS_FOR_TRANSLATION; за замовчуванням INGEST_THREADS=1.
5. `ingest.py`: захист від порожнього SOURCE_DOCUMENTS (уникнення падіння).
6. `stream_server.py`: debug=False.
7. `run_server.py`: no_proxy="*" закоментовано; помилка написання "breast canser" → "breast cancer".

## Зміни, що НЕ було впроваджено (потребує числової валідації/регресії)
- REA-005: ініціалізація Chroma на рівні модуля.
- REA-006: перевірка облікових даних.
- REA-007: видалити verbose=True (логи з даними про здоров'я).
- REA-008: закріплення версій duckdb/pandas/pyarrow + smoke test ingest.
- REA-013: обмеження працівників ThreadPoolExecutor.
- REA-015: автентифікація/обмеження швидкості на кінцевих точках.

## Виконана валідація
- `python -m py_compile` OK на model_property.py, ingest.py, run_server.py, stream_server.py, wsgi.py
- Не виконано: ingest/server/benchmark (відсутні залежності)

## Залишаючіся ризики
- Облікові дані OpenAI можуть бути вже розкриті в історії (medlocalgpt.env відслідковується з старих комітів); рекомендується ротація ключів.
- Збирання/ingest не валідовано (средовище без залежностей).

## Рекомендації для майбутніх аудитів
- Ротація OPENAI_API_KEY/OPENAI_ORGANIZATION.
- Встановити залежності та запустити smoke test ingest (порожній каталог + 1 документ).
- Додати pytest + CI.
- Додати автентифікацію/обмеження швидкості на кінцевих точках.
