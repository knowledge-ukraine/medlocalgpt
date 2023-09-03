# ⚕️ medlocalgpt

Applying LLM-powered (OpenAI GPT-4, Vicuna, Orca-mini, etc.) AI Assistant to Enhance Support for Physical Rehabilitation & Telerehabilitation Therapists, Students, and Patients.
Ask your EBSCO dataset (domain knowledge: rehabilitation medicine) using LLMs and Embeddings. Optionally you can use local LLMs, OpenAI GPT models or other SaaS solutions via [LangChain](https://github.com/hwchase17/langchain).

This project is part of the R&D on intelligent data analysis and computational linguistics for digital health (telerehabilitation an rehabilitation medicines). Read more: [Letter to the Editor–Update from Ukraine: Development of the Cloud-based Platform for Patient-centered Telerehabilitation of Oncology Patients with Mathematical-related Modeling](https://doi.org/10.5195/ijt.2023.6562).

## Sponsor this project

Please support @malakhovks. Despite the Wartime in Ukraine, R&D in the field of Digital Health are being resumed.
[https://send.monobank.ua/jar/5ad56oNAcD](https://send.monobank.ua/jar/5ad56oNAcD)

## Inspired by

This project was inspired by the original [privateGPT](https://github.com/imartinez/privateGPT) and [localGPT](https://github.com/PromtEngineer/localGPT).

Built with [🦜️🔗 LangChain](https://github.com/hwchase17/langchain), [GPT4All](https://github.com/nomic-ai/gpt4all), [LlamaCpp](https://github.com/ggerganov/llama.cpp), [Chroma](https://www.trychroma.com/), [SentenceTransformers](https://www.sbert.net/), [InstructorEmbeddings](https://instructor-embedding.github.io/).

## ⚠️ Important note

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

### Query to OpenAI models with tuning prompt (domain knowledge, OpenAI model, max tokens generation, temperature - all this sets up with `medlocalgpt.env`) in English only

**Request:**

`POST /medlocalgpt/api/v1/en/advanced/openai/ask`

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

```json
{
  "prompt": "What are the ICD-10 codes for abdominal aortic aneurysm?",
  "response": "Abdominal aortic aneurysm is a potentially life-threatening condition characterized by the weakening and bulging of the abdominal aorta, the largest artery in the body. The International Classification of Diseases, 10th Revision (ICD-10) provides specific codes to classify and document this condition. The ICD-10 codes for abdominal aortic aneurysm are as follows:\n\n1. I71.4 - Abdominal aortic aneurysm, without rupture\n2. I71.5 - Abdominal aortic aneurysm, ruptured\n\nThese codes are used to accurately identify and classify cases of abdominal aortic aneurysm in medical records, billing, and research. It is important for healthcare professionals to use these codes to ensure proper documentation and communication of the condition.\n\nPlease note that these codes are specific to abdominal aortic aneurysm and should not be used for other types of aneurysms or conditions. It is always recommended to consult the official ICD-10 coding guidelines and documentation for accurate coding and billing practices.\n\nIf you have any further questions or need more information, feel free to ask."
}
```

## 🗃️ Dataset

EBSCO articles dataset (domain knowledge: rehabilitation medicine) + JSON of every article

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8308214.svg)](https://doi.org/10.5281/zenodo.8308214)

```bash
wget -O ./ebsco-rehabilitation-dataset.zip https://cdn.e-rehab.pp.ua/u/ebsco-rehabilitation-dataset.zip
```
