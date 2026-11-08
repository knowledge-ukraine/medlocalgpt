# REVERSE ENGINEERING REPORT — knowledge-ukraine/medlocalgpt

## Original repository
- Name: medlocalgpt
- URL: https://github.com/knowledge-ukraine/medlocalgpt
- Type: LLM-powered RAG assistant for physical rehabilitation & telerehabilitation (Flask + LangChain + Chroma)
- Branch: master
- Base: 14efc95 docs: update project funding details (#23)

## Audit date
2026-11-07

## Tools used
- Git v2.49.0
- PowerShell 5.1
- gh (GitHub CLI), authenticated as admeduardovieira
- Kilo Code (static analysis of Python/YAML files)
- python 3.12.14 (py_compile only — syntax)

## Identified architecture
Flask application with RAG (Retrieval-Augmented Generation) pipeline over a rehabilitation dataset (EBSCO).
Components:
- run_server.py: Flask API, LangChain chains (OpenAI/local), Chroma retriever, routes /medlocalgpt/api/v1/*/ask
- ingest.py: loads SOURCE_DOCUMENTS, performs chunking (RecursiveCharacterTextSplitter), embeds with HuggingFaceInstructEmbeddings, persists Chroma (duckdb+parquet)
- model_property.py: configuration via environment variables (medlocalgpt.env)
- stream_server.py: LangChain streaming example (debug=True)
- wsgi.py / deploy/uwsgi.ini / docker-compose.yml / deploy/nginx.conf: production
- Frontend: templates/index.html + static/ (JS/CSS)

## Technologies and dependencies
Python 3.10, Flask, LangChain 0.0.191, Chroma 0.3.22 (duckdb+parquet), OpenAI SDK, googletrans, sentence-transformers, llama-cpp-python, auto-gptq, uWSGI, nginx.
requirements.txt without proper pinning; deploy/requirements.txt duplicated.

## Maintenance status
- 1 open issue (#20, duckdb/pandas, 2023-09-04, still unresolved)
- 23 PRs (all merged; #2 "Fixed exposed openai token" — evidence of prior credential exposure)
- Last functional activity: 2023-09; docs: 2025-09
- No automated tests, no CI, no pytest

## Investigation limitations
- No Python environment with dependencies (langchain, chromadb, torch, etc.) to run ingest/server/benchmarks
- Not an FHIR/SUSHI project (releaselabel rules do not apply)

---

## Problems found (medlocalgpt)

| ID | Sev | Status | Location | Problem | Fix applied |
|---|---|---|---|---|---|
| REA-001 | P0 | CONFIRMED | medlocalgpt.env (tracked), .gitignore | Environment file with OPENAI_API_KEY/OPENAI_ORGANIZATION versioned; .gitignore ignores only .env, not medlocalgpt.env | .gitignore ignores medlocalgpt.env + SOURCE_DOCUMENTS/ (except .gitkeep); .env.example with placeholders |
| REA-002 | P1 | CONFIRMED | model_property.py:44 | MAX_TOKENS_OPENAI reads os.environ['MAX_TOKENS'] (wrong variable) | Reads MAX_TOKENS_OPENAI |
| REA-003 | P1 | CONFIRMED | model_property.py:49 | MAX_TOKENS_FOR_TRANSLATION reads os.environ['MAX_TOKENS'] (wrong variable) | Reads MAX_TOKENS_FOR_TRANSLATION |
| REA-004 | P1 | CONFIRMED | ingest.py:58-63 | SOURCE_DOCUMENTS empty → chunksize=0 → range(0,0,0) ValueError | Guards empty paths; minimum chunksize 1 |
| REA-005 | P2 | CONFIRMED | run_server.py:150-155 | EMBEDDINGS/DB (Chroma) instantiated at module level; load_model failure blocks server | Not fixed in this round (requires regression) |
| REA-006 | P2 | CONFIRMED | run_server.py:167 | Confusing credential validation (is not None; does not reject empty strings) | Not fixed in this round |
| REA-007 | P2 | PROBABLE | run_server.py:364 | SimpleSequentialChain verbose=True logs prompts/responses (potential health data) | Not fixed in this round |
| REA-008 | P2 | CONFIRMED | requirements.txt / deploy/requirements.txt / Issue #20 | duckdb/pandas/pyarrow incompatibility; issue open since 2023-09-04 | Not fixed in this round (requires pins + smoke test) |
| REA-009 | P3 | CONFIRMED | medlocalgpt.env:6; run_server.py:329 | Typo "breast canser" | Fixed to "breast cancer" |
| REA-010 | P2 | CONFIRMED | stream_server.py:94; run_server.py:4 | stream_server.py debug=True (exposes stack traces); run_server.py no_proxy="*" (bypasses proxy/firewall) | debug=False; no_proxy commented |
| REA-011 | P3 | CONFIRMED | model_property.py:94 | INGEST_THREADS = os.cpu_count() can be None → TypeError | Default 1 when None |
| REA-012 | P3 | CONFIRMED | requirements.txt | Dependencies without proper pinning; Streamlit-extras wrong name; InstructorEmbedding doubtful | Not fixed in this round |
| REA-013 | P3 | CONFIRMED | ingest.py:37 | ThreadPoolExecutor(len(filepaths)) — unlimited threads | Not fixed in this round |
| REA-014 | P3 | CONFIRMED | .gitignore; SOURCE_DOCUMENTS/constitution.pdf | User documents directory not ignored; constitution.pdf (potential PHI) tracked | SOURCE_DOCUMENTS/ ignored (except .gitkeep); constitution.pdf remains tracked (already versioned) |
| REA-015 | P3 | HYPOTHESIS | run_server.py routes | Missing authentication/rate-limit on API endpoints | Not fixed in this round |

## Recurring problems
1. duckdb/pandas incompatibility (Issue #20) — opened 2023-09-04, still unresolved; fix pandas commits did not prevent persistence.
2. Credential exposure (PR #2) — already occurred; medlocalgpt.env still tracked (risk persists).

## Undocumented errors (new from audit)
REA-002, REA-003, REA-004, REA-005, REA-006, REA-009, REA-010, REA-011, REA-013, REA-014, REA-015 have no visible public record.

## Changes implemented (Phase 2)
1. `.gitignore`: ignores medlocalgpt.env and SOURCE_DOCUMENTS/ (keeps .gitkeep); constitution.pdf already tracked remains.
2. `.env.example` (new): placeholders without real keys.
3. `SOURCE_DOCUMENTS/.gitkeep` (new): keeps empty directory tracked.
4. `model_property.py`: fixes reading of MAX_TOKENS_OPENAI / MAX_TOKENS_FOR_TRANSLATION; default INGEST_THREADS=1.
5. `ingest.py`: guards empty SOURCE_DOCUMENTS (avoids crash).
6. `stream_server.py`: debug=False.
7. `run_server.py`: no_proxy="*" commented out; typo "breast canser"→"breast cancer".

## Changes NOT implemented (require numeric validation/regression)
- REA-005: Chroma initialization at module level.
- REA-006: credential validation.
- REA-007: remove verbose=True (logs with health data).
- REA-008: duckdb/pandas/pyarrow pins + ingest smoke test.
- REA-013: limit ThreadPoolExecutor workers.
- REA-015: authentication/rate-limit on endpoints.

## Validation performed
- `python -m py_compile` OK on model_property.py, ingest.py, run_server.py, stream_server.py, wsgi.py
- Not executed: ingest/server/benchmark (missing dependencies)

## Remaining risks
- OpenAI credentials may already have been exposed in history (medlocalgpt.env tracked since old commits); recommend rotating keys.
- Build/ingest not validated (environment without dependencies).

## Recommendations for future audits
- Rotate OPENAI_API_KEY/OPENAI_ORGANIZATION.
- Install dependencies and run ingest smoke test (empty directory + 1 document).
- Add pytest + CI.
- Add authentication/rate-limit on endpoints.
