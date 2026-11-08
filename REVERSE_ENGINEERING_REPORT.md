# REVERSE ENGINEERING REPORT — knowledge-ukraine/medlocalgpt

## Repositório original
- Nome: medlocalgpt
- URL: https://github.com/knowledge-ukraine/medlocalgpt
- Tipo: LLM-powered RAG assistant for physical rehabilitation & telerehabilitation (Flask + LangChain + Chroma)
- Branch: master
- Base: 14efc95 docs: update project funding details (#23)

## Data da auditoria
2026-11-07

## Ferramentas utilizadas
- Git v2.49.0
- PowerShell 5.1
- gh (GitHub CLI), autenticado como admeduardovieira
- Kilo Code (análise estática de arquivos Python/YAML)
- python 3.12.14 (py_compile apenas — sintaxe)

## Arquitetura identificada
Aplicação Flask com pipeline RAG (Retrieval-Augmented Generation) sobre dataset de reabilitação (EBSCO).
Componentes:
- run_server.py: API Flask, chains LangChain (OpenAI/local), Chroma retriever, rotas /medlocalgpt/api/v1/*/ask
- ingest.py: carrega SOURCE_DOCUMENTS, faz chunking (RecursiveCharacterTextSplitter), embarca com HuggingFaceInstructEmbeddings, persiste Chroma (duckdb+parquet)
- model_property.py: configuração por variáveis de ambiente (medlocalgpt.env)
- stream_server.py: exemplo de streaming LangChain (debug=True)
- wsgi.py / deploy/uwsgi.ini / docker-compose.yml / deploy/nginx.conf: produção
- Frontend: templates/index.html + static/ (JS/CSS)

## Tecnologias e dependências
Python 3.10, Flask, LangChain 0.0.191, Chroma 0.3.22 (duckdb+parquet), OpenAI SDK, googletrans, sentence-transformers, llama-cpp-python, auto-gptq, uWSGI, nginx.
requirements.txt sem pin adequado; deploy/requirements.txt duplicado.

## Estado de manutenção
- 1 Issue aberta (#20, duckdb/pandas, 2023-09-04, ainda não resolvida)
- 23 PRs (todos mergados; #2 "Fixed exposed openai token" — evidência de exposição prévia de credenciais)
- Última atividade funcional: 2023-09; docs: 2025-09
- Sem testes automatizados, sem CI, sem pytest

## Limitações da investigação
- Sem ambiente Python com dependências (langchain, chromadb, torch, etc.) para executar ingest/server/benchmarks
- Não é projeto FHIR/SUSHI (regras de releaselabel não se aplicam)

---

## Problemas encontrados (medlocalgpt)

| ID | Sev | Status | Local | Problema | Correção aplicada |
|---|---|---|---|---|---|
| REA-001 | P0 | CONFIRMADO | medlocalgpt.env (rastreado), .gitignore | Arquivo de ambiente com OPENAI_API_KEY/OPENAI_ORGANIZATION versionado; .gitignore ignora apenas .env, não medlocalgpt.env | .gitignore ignora medlocalgpt.env + SOURCE_DOCUMENTS/ (exceto .gitkeep); .env.example com placeholders |
| REA-002 | P1 | CONFIRMADO | model_property.py:44 | MAX_TOKENS_OPENAI lê os.environ['MAX_TOKENS'] (variável errada) | Lê MAX_TOKENS_OPENAI |
| REA-003 | P1 | CONFIRMADO | model_property.py:49 | MAX_TOKENS_FOR_TRANSLATION lê os.environ['MAX_TOKENS'] (variável errada) | Lê MAX_TOKENS_FOR_TRANSLATION |
| REA-004 | P1 | CONFIRMADO | ingest.py:58-63 | SOURCE_DOCUMENTS vazio → chunksize=0 → range(0,0,0) ValueError | Guarda caminhos vazios; chunksize mínimo 1 |
| REA-005 | P2 | CONFIRMADO | run_server.py:150-155 | EMBEDDINGS/DB (Chroma) instanciados no nível do módulo; falha no load_model impede o servidor | Não corrigido nesta rodada (requer regressão) |
| REA-006 | P2 | CONFIRMADO | run_server.py:167 | Validação de credenciais confusa (is not None; não rejeita strings vazias) | Não corrigido nesta rodada |
| REA-007 | P2 | PROVÁVEL | run_server.py:364 | SimpleSequentialChain verbose=True loga prompts/respostas (dados de saúde potenciais) | Não corrigido nesta rodada |
| REA-008 | P2 | CONFIRMADO | requirements.txt / deploy/requirements.txt / Issue #20 | Incompatibilidade duckdb/pandas/pyarrow; issue aberta desde 2023-09-04 | Não corrigido nesta rodada (requer pins + smoke test) |
| REA-009 | P3 | CONFIRMADO | medlocalgpt.env:6; run_server.py:329 | Typo "breast canser" | Corrigido para "breast cancer" |
| REA-010 | P2 | CONFIRMADO | stream_server.py:94; run_server.py:4 | stream_server.py debug=True (expõe stack traces); run_server.py no_proxy="*" (bypass proxy/firewall) | debug=False; no_proxy comentado |
| REA-011 | P3 | CONFIRMADO | model_property.py:94 | INGEST_THREADS = os.cpu_count() pode ser None → TypeError | Default 1 quando None |
| REA-012 | P3 | CONFIRMADO | requirements.txt | Dependências sem pin adequado; Streamlit-extras nome errado; InstructorEmbedding duvidoso | Não corrigido nesta rodada |
| REA-013 | P3 | CONFIRMADO | ingest.py:37 | ThreadPoolExecutor(len(filepaths)) — threads ilimitadas | Não corrigido nesta rodada |
| REA-014 | P3 | CONFIRMADO | .gitignore; SOURCE_DOCUMENTS/constitution.pdf | Diretório de documentos do usuário não ignorado; constitution.pdf (potencial PHI) rastreado | SOURCE_DOCUMENTS/ ignorado (exceto .gitkeep); constitution.pdf permanece tracked (já versionado) |
| REA-015 | P3 | HIPÓTESE | run_server.py rotas | Ausência de autenticação/rate-limit nos endpoints de API | Não corrigido nesta rodada |

## Problemas recorrentes
1. Incompatibilidade duckdb/pandas (Issue #20) — aberta 2023-09-04, ainda não resolvida; commits fix pandas não impediram a persistência.
2. Exposição de credenciais (PR #2) — já ocorreu; medlocalgpt.env continua rastreado (risco persiste).

## Erros não documentados (novos da auditoria)
REA-002, REA-003, REA-004, REA-005, REA-006, REA-009, REA-010, REA-011, REA-013, REA-014, REA-015 não têm registro público visível.

## Mudanças implementadas (Fase 2)
1. .gitignore: ignora medlocalgpt.env e SOURCE_DOCUMENTS/ (mantém .gitkeep); constitution.pdf já trackeado permanece.
2. .env.example (novo): placeholders sem chaves reais.
3. SOURCE_DOCUMENTS/.gitkeep (novo): mantém diretório vazio trackeado.
4. model_property.py: corrige leitura de MAX_TOKENS_OPENAI / MAX_TOKENS_FOR_TRANSLATION; default INGEST_THREADS=1.
5. ingest.py: guarda SOURCE_DOCUMENTS vazio (evita crash).
6. stream_server.py: debug=False.
7. run_server.py: no_proxy="*" comentado; typo "breast canser"→"breast cancer".

## Mudanças NÃO implementadas (requerem validação numérica/regressão)
- REA-005: inicialização do Chroma no nível do módulo.
- REA-006: validação de credenciais.
- REA-007: remover verbose=True (logs com dados de saúde).
- REA-008: pins de duckdb/pandas/pyarrow + smoke test de ingest.
- REA-013: limitar workers do ThreadPoolExecutor.
- REA-015: autenticação/rate-limit nos endpoints.

## Validação executada
- python -m py_compile OK em model_property.py, ingest.py, run_server.py, stream_server.py, wsgi.py
- Não executado: ingest/server/benchmark (dependências ausentes)

## Riscos remanescentes
- Credenciais OpenAI já podem ter sido expostas em histórico (medlocalgpt.env rastreado desde commits antigos); recomenda-se rotacionar chaves.
- Build/ingest não validado (ambiente sem dependências).

## Recomendações para auditorias futuras
- Rotacionar OPENAI_API_KEY/OPENAI_ORGANIZATION.
- Instalar dependências e executar smoke test de ingest (diretório vazio + 1 documento).
- Adicionar pytest + CI.
- Adicionar autenticação/rate-limit nos endpoints.
