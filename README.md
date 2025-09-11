# ⚕️ medlocalgpt

Applying LLM-powered (OpenAI GPT-4, Vicuna, Orca-mini, etc.) AI Assistant to Enhance Support for Physical Rehabilitation & Telerehabilitation Therapists, Students, and Patients.
Ask your EBSCO dataset (domain knowledge: rehabilitation medicine) using LLMs and Embeddings. Optionally you can use local LLMs, OpenAI GPT models or other SaaS solutions via [🦜️🔗 LangChain](https://github.com/hwchase17/langchain).

This project is part of the R&D on intelligent data analysis and computational linguistics for digital health (telerehabilitation and rehabilitation medicines). Read more: [Letter to the Editor–Update from Ukraine: Development of the Cloud-based Platform for Patient-centered Telerehabilitation of Oncology Patients with Mathematical-related Modeling](https://doi.org/10.5195/ijt.2023.6562).

Supported languges: English, Ukrainian

## 📖 Quick index
  * [🚀 Sponsor this project](#-sponsor-this-project)
  * [🌎 Inspired by](#-inspired-by)
  * [⚠ Important note](#-important-note)
  * [💻 Setup for Testing](#-setup-for-testing)
  * [💻 Setup for Production](#-setup-for-production)
  * [🎈 API usage](#-api-usage)
  * [📕 Dataset](#-dataset)
  * [🏥 MedLocalGPT Project Case: CPU-only Multi-Agent Deployment for Telerehabilitation](#medlocalgpt-project-case-cpu-only-multi-agent-deployment-for-telerehabilitation)

## 🚀 Sponsor this project

Please support @malakhovks. Despite the Wartime in Ukraine, R&D in the field of Digital Health are being resumed.
[https://send.monobank.ua/jar/5ad56oNAcD](https://send.monobank.ua/jar/5ad56oNAcD)

## 🌎 Inspired by

This project was inspired by the original [privateGPT](https://github.com/imartinez/privateGPT) and [localGPT](https://github.com/PromtEngineer/localGPT).

Built with [🦜️🔗 LangChain](https://github.com/hwchase17/langchain), [GPT4All](https://github.com/nomic-ai/gpt4all), [LlamaCpp](https://github.com/ggerganov/llama.cpp), [Chroma](https://www.trychroma.com/), [SentenceTransformers](https://www.sbert.net/), [InstructorEmbeddings](https://instructor-embedding.github.io/).

## ⚠ Important note

**medlocalgpt** project and documentation are in active development. For any technical clarifications and questions contact me via email: [malakhovks@nas.gov.ua](mailto:malakhovks@nas.gov.ua) or via Issues. The recent Russian's rocket shelling on critical infrastructure in Ukraine and Kyiv led our server infrastructure to become unstable.
**CPU support only (for now)**

## 💻 Setup for Testing

### 🐍 Environment setup

1. Install Mininconda

    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    ```

    ```bash
    bash Miniconda3-latest-Linux-x86_64.sh
    ```

2. Create Conda environment

    ```bash
    conda create -n medlocalgpt python=3.10.12
    ```

3. Activate Conda environment

    ```bash
    conda activate medlocalgpt
    ```

4. Install requirements

    ```bash
    pip install -r requirements.txt
    ```

5. Set environment variables

    Set environment variables from `medlocalgpt.env` file of key/value pairs:

    ```bash
    set -o allexport && source medlocalgpt.env && set +o allexport
    ```

    You can do it manually.

    Set embedding model:

    ```bash
    export EMBEDDING_MODEL_NAME="hkunlp/instructor-large"
    ```

    Set LLM repo:

    ```bash
    export MODEL_ID="TheBloke/orca_mini_3B-GGML"
    ```

    Set LLM's base name:

    ```bash
    export MODEL_BASENAME="orca-mini-3b.ggmlv3.q4_0.bin"
    ```

    Set returned source documents number:

    ```bash
    export DOC_NUMBER=6
    ```

    Set max response lenth:

    ```bash
    export MAX_TOKENS=256
    ```

    Set OpenAI cridentials and model:

    ```bash
    export OPENAI_API_KEY="YOUR API KEY"
    ```

    ```bash
    export OPENAI_ORGANIZATION="YOUR ORGNIZATION ID"
    ```

    ```bash
    export OPENAI_MODEL="gpt-3.5-turbo-16k"
    ```

    Set domain knowledge:

    ```bash
    export SUBJECT="medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research"
    ```

6. Put all of your documents (.txt, .pdf, or .csv) into the SOURCE_DOCUMENTS and ingest all the data

    ⚠️ **CPU USAGE CAUTION**

    First of you need a lot of CPU cores to processing (to ingest) more documents. The week point here is not a RAM size.
    Also the **week point is the memory bandwidth**. That's why all this stuff working great on M1 or M2 chip.
    Read more about that you can here: [How is LLaMa.cpp possible?](https://finbarr.ca/how-is-llama-cpp-possible/)

    **PS:**  I also have a couple of HP servers, and using 28 cores, 1000 PDFs processed about 6 hours.

    ```bash
    python ingest.py
    ```

    **Default models**

    - Embedding model: `hkunlp/instructor-large` from [InstructorEmbeddings](https://instructor-embedding.github.io/)
    - LLM: `orca-mini-3b.ggmlv3.q4_0.bin` from [TheBloke/orca_mini_3B-GGML](https://huggingface.co/TheBloke/orca_mini_3B-GGML)

7. Run medlocalgpt service

    ```bash
    python run_server.py
    ```

## 💻 Setup for Production

TODO

## 🎈 API usage

### Query to OpenAI models with tuning prompt (domain knowledge, OpenAI model, max tokens generation, temperature - all this sets up with `medlocalgpt.env`)

**Request:**

Query language: English

Endpoint: `/medlocalgpt/api/v1/en/advanced/openai/ask`

```javascript
    const API_URL = "/medlocalgpt/api/v1/en/advanced/openai/ask"
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: "What are the ICD-10 codes for abdominal aortic aneurysm?"
        })
    }
    const response = await (await fetch(API_URL, requestOptions)).json();
```

**Response:**

```JSON
{
  "prompt": "What are the ICD-10 codes for abdominal aortic aneurysm?",
  "response": "Abdominal aortic aneurysm is a potentially life-threatening condition characterized by the weakening and bulging of the abdominal aorta, the largest artery in the body. The International Classification of Diseases, 10th Revision (ICD-10) provides specific codes to classify and document this condition. The ICD-10 codes for abdominal aortic aneurysm are as follows:\n\n1. I71.4 - Abdominal aortic aneurysm, without rupture\n2. I71.5 - Abdominal aortic aneurysm, ruptured\n\nThese codes are used to accurately identify and classify cases of abdominal aortic aneurysm in medical records, billing, and research. It is important for healthcare professionals to use these codes to ensure proper documentation and communication of the condition.\n\nPlease note that these codes are specific to abdominal aortic aneurysm and should not be used for other types of aneurysms or conditions. It is always recommended to consult the official ICD-10 coding guidelines and documentation for accurate coding and billing practices.\n\nIf you have any further questions or need more information, feel free to ask."
}
```

------

### Query to EBSCO articles dataset with tuning prompt (domain knowledge, OpenAI model, max tokens generation, temperature - all this sets up with `medlocalgpt.env`) using OpenAI models

**Request:**

Query language: English

Endpoint: `/medlocalgpt/api/v1/en/dataset/openai/ask`

```javascript
    const API_URL = "/medlocalgpt/api/v1/en/dataset/openai/ask"
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: "What are the ICD-10 codes for abdominal aortic aneurysm?"
        })
    }
    const response = await (await fetch(API_URL, requestOptions)).json();
```

**Response:**

```JSON
{
  "Answer": "The ICD-10 codes for abdominal aortic aneurysm are I71.3 for ruptured abdominal aortic aneurysm and I71.4 for abdominal aortic aneurysm without mention of rupture.",
  "Prompt": "What are the ICD-10 codes for abdominal aortic aneurysm?",
  "Sources": [
    [
      "Abdominal Aorta Aneurysm.pdf",
      "https://cdn.e-rehab.pp.ua/u/Abdominal%20Aorta%20Aneurysm.pdf",
      "• I71.3 abdominal aortic aneurysm, ruptured\n• I71.4 abdominal aortic aneurysm, without mention of rupture\n\nAuthor\nRudy Dressendorfer, BScPT, PhD\nCinahl Information Systems, Glendale, CA\n\nReviewer\nEllenore Palmer, BScPT, MSc\nCinahl Information Systems, Glendale, CA\n\nEditor\nSharon Richman, MSPT\nCinahl Information Systems, Glendale, CA\n\nApril 21, 2017"
    ],
    [
      "Abdominal Aorta Aneurysm.pdf",
      "https://cdn.e-rehab.pp.ua/u/Abdominal%20Aorta%20Aneurysm.pdf",
      "Coding Matrix\nReferences are rated using the following codes, listed in order of strength:\n\nM Published meta-analysis\n\nRV Published review of the literature\n\nSR Published systematic or integrative literature review\n\nRU Published research utilization report\n\nPP Policies, procedures, protocols\n\nX Practice exemplars, stories, opinions\n\nRCT Published research (randomized controlled trial)\n\nQI Published quality improvement report\n\nGI General or background information/texts/reports\n\nR Published research (not randomized controlled trial)\n\nL Legislation\n\nC Case histories, case studies\n\nG Published guidelines\n\nPGR Published government report\n\nPFR Published funded report\n\nU Unpublished research, reviews, poster presentations or\n\nother such materials\n\nCP Conference proceedings, abstracts, presentation\n\nReferences\n1. Sakalihasan N, Limet R, Defawe OD. Abdominal aortic aneurysm. Lancet . 2005;365(9470):1577-89. (RV)"
    ],
    [
      "Abdominal Aorta Aneurysm.pdf",
      "https://cdn.e-rehab.pp.ua/u/Abdominal%20Aorta%20Aneurysm.pdf",
      "other such materials\n\nCP Conference proceedings, abstracts, presentation\n\nReferences\n1. Sakalihasan N, Limet R, Defawe OD. Abdominal aortic aneurysm. Lancet . 2005;365(9470):1577-89. (RV)\n\n2. Braverman AC. Diseases of the aorta. In: Mann DL, Zipes DP, Libbyt P, Bonow RO, Braunwald E, eds. Braunwald’s Heart Disease: a textbook of cardiovascular medicine .\n\n10th ed. Philadelphia, PA: Elsevier Saunders; 2015:1278-82. (GI)\n\n3. Rooke TW, Hirsch AT, Misra S, et al. 2011 ACCF/AHA focused update of the guideline for the management of patients with peripheral artery diease (updating the 2005\n\nguideline): a report of the American College of Cardiology Foundation/American Heart Association Task Force on Practice Guidelines. Circulation. 2011;124(18):2020-2045.\ndoi:10.1161/CIRC.0b013e31822e80c3.  (G)\n\n4. Rughani G, Robertson L, Clarke M. Medical treatment for small abdominal aortic aneurysms. Cochrane Database Syst Rev. September 12, 2012;CD009536.\n\ndoi:10.1002/14651858.CD009536.pub2. (SR)"
    ],
    [
      "Abdominal Aorta Aneurysm.pdf",
      "https://cdn.e-rehab.pp.ua/u/Abdominal%20Aorta%20Aneurysm.pdf",
      "CLINICAL\nREVIEW\n\nAbdominal Aorta Aneurysm\n\nIndexing Metadata/Description\n› Title/condition: Abdominal Aortic Aneurysm\n› Synonyms: Infrarenal aortic aneurysm, juxtarenalaortic aneurysm, atherosclerotic\n\nabdominal aortic aneurysm, inflammatory abdominal aortic aneurysm\n\n› Anatomical location/body part affected: Abdomen/infrarenal aorta; may include\n\ncommon iliac artery\n\n› Area(s) of specialty: Acute Care, Cardiovascular Rehabilitation, Geriatric Medicine\n› Description\n\n• Abdominal aortic aneurysm (AAA) is an abnormal dilation in the arterial wall that arises\nbelow the thorax, usually (95% of the time) below branches of the renal arteries(1,2,3)\n• In general,AAAs are identified on diagnostic ultrasound screening as an"
    ],
    [
      "Abdominal Aorta Aneurysm.pdf",
      "https://cdn.e-rehab.pp.ua/u/Abdominal%20Aorta%20Aneurysm.pdf",
      "• AAA is an asymptomatic condition. However, patients are at risk of cardiovascular\n\ndisease (CVD) and do require increased caution for CVD symptoms. The chief\nconcern in patients with a small AAA is to maintain regular activities of daily living\n(ADLs),promote health-related physical fitness, and encourage periodic ultrasound\nsurveillance(1,5)\n• Prophylactic prescribed aerobic exercise for patients awaiting elective AAA surgical\nrepair may favorably reduce post-operativecomplications and improve survival at\n3-years follow-up(5,6,7,8)\n• Supervised exercise training may provide clinical benefits without complications in\nselected patients with a small AAA(9,10)\n\n› ICD-9 codes\n\n• 441.3 abdominal aneurysm, ruptured\n• 441.4 abdominal aneurysm without mention of rupture\n\n› ICD-10 codes\n\n• I71.3 abdominal aortic aneurysm, ruptured\n• I71.4 abdominal aortic aneurysm, without mention of rupture\n\nAuthor\nRudy Dressendorfer, BScPT, PhD\nCinahl Information Systems, Glendale, CA"
    ],
    [
      "Abdominal Aorta Aneurysm.pdf",
      "https://cdn.e-rehab.pp.ua/u/Abdominal%20Aorta%20Aneurysm.pdf",
      "18. Majeed K, Hamer AW, White SC, et al. Prevalence of abdominal aortic aneurysm in patients referred for transthoracic echocardiography. Intern Med J. 2015;45(1):32-39.\n\ndoi:10.1111/imj.12592. (R)\n\n19. Nagai S, Kudo T, Inoue Y, Akaza M, Sasano T, Sumi Y. Preoperative predictors of long-term mortality after elective endovascular aneurysm repair for abdominal aortic\n\naneurysm. Ann Vasc Dis. 2016;9(1):42-47. doi:10.3400/avd.oa.15-00129. (R)\n\n20. Komai H, Shindo S, Sato M, Ogino H. Reduced protein C activity might be associated with progression of peripheral arterial disease. Angiology. 2015;66(6):584-587.\n\ndoi:10.1177/0003319714544946. (R)\n\n21. RESCAN Collaborators, Brown MJ, Sweeting MJ, Brown LC, Powell JT, Thompson SG. Surveillance intervals for small abdominal aortic aneurysms: a meta-analysis.\n\n2013;309(8):806-813. doi:10.1001/jama.2013.950. (M)"
    ]
  ]
}
```

## 📕 Dataset

EBSCO articles dataset (domain knowledge: rehabilitation medicine) + JSON of every article

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8308214.svg)](https://doi.org/10.5281/zenodo.8308214)

```bash
wget -O ./ebsco-rehabilitation-dataset.zip https://cdn.e-rehab.pp.ua/u/ebsco-rehabilitation-dataset.zip
```

## MedLocalGPT Project Case: CPU-only Multi-Agent Deployment for Telerehabilitation

The MedLocalGPT system (Figure 1) serves therapists, students, and patients through a web application that orchestrates two llama.cpp–based agents and a vector database. The first agent performs bidirectional English↔Ukrainian translation using Phi-4-mini-instruct (3.8B, Q4 GGUF). The second agent handles domain Q&A and lightweight reasoning using Gemma-3-1B-it (Q4 GGUF). A semantic index built with a high-quality Instructor embedding model feeds a ChromaDB vector store; the retrieval layer operates over a curated EBSCO rehabilitation-medicine dataset (peer-reviewed articles), enabling RAG for grounded responses.

![C4 context/container diagram for the MedLocalGPT system. The web application orchestrates two llama.cpp agents (EN↔UK translation with Phi-4-mini-instruct; Q&A and reasoning with Gemma-3-1B-it) and a RAG pipeline over a ChromaDB vector store populated from an EBSCO rehabilitation-medicine corpus.](static/images/medlocalgpt_c4_diagram.png)

**Models selection.** *Phi-4-mini-instruct* offers strong instruction following and competitive small-model translation quality under CPU constraints; at 4-bit it fits in ~1.9 GB RAM and sustains ~15 tok/s on an E5-2695 v2–class host and ~40–80 tok/s on modern laptop/new-Xeon CPUs. This makes sentence-level EN↔UK translation responsive while preserving headroom for concurrent services. *Gemma-3-1B-it* (~0.6 GB at Q4) is selected for Q&A to maximize throughput tok/s and minimize latency for short, fact-seeking prompts; typical rates are ~30 tok/s (E5-class) and 70–100 tok/s (laptop/new-Xeon), adequate for interactive clinical-education use. The small memory footprints allow both agents, the embedding service, and the database to co-reside on a 16-vCPU/32 GB KVM VM without swapping, while the *Intel oneAPI (oneMKL)* build of *llama.cpp* provides consistent BLAS performance in the containerized runtime.

**RAG over EBSCO dataset.** The ingestion pipeline extracts text from EBSCO articles, normalizes typography, and applies domain-aware chunking (target 512–768 tokens with 15–20 % overlap) to preserve local cohesion around methods and results sections. Each chunk is embedded with an Instructor-large model; the store maintains cosine similarity vectors and metadata (journal, year, DOI, MeSH-like tags). Prompts given to the Q&A agent include: the user question, top-k chunks with citations, a grounding instruction (answer strictly from the provided passages; otherwise say – insufficient evidence), and formatting constraints suitable for clinical or educational contexts. For bilingual sessions, the translation agent post-processes answers to the target language and preserves clinical terminology via a prompt-level glossary.

**Latency and concurrency on CPU.** On the 16-vCPU VM, practical allocation dedicates 6 vCPUs to the Q&A agent and 7 vCPUs to the translation agent, leaving the remainder to the embedding/query layer and the web API. With this partitioning and Q4 quantization, median end-to-end latency for short, grounded answers (~80–120 generated tokens, k=8 context chunks) is typically ~2.5–4.5 s on an E5-class host and <2 s on a newer Xeon. For translation, sentence-level round-trips (15–25 tokens) complete in ~1–3 s depending on CPU class. To sustain multi-user access, the deployment favors multi-process concurrency (one llama.cpp server per agent) with CPU affinity and NUMA pinning; for small prompts, running two parallel Q&A workers can increase throughput more than a single worker using all cores.

The CPU-only design simplifies procurement and on-premises deployment for sensitive data, while the small-model agents lower energy draw and cost. Overall, the architecture delivers grounded, bilingual assistance for rehabilitation medicine with predictable latency on commodity CPUs, matching the project’s privacy and cost constraints.

