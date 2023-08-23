# medlocalgpt

Ask your (medical) dataset privately using LLMs and Embeddings. No data leaves your infrastructure/platform and 100% private.
Optionally you can use OpenAI GPT models or other LLM SaaS solutions via [LangChain](https://github.com/hwchase17/langchain).

This project is part of the R&D on intelligent data analysis and computational linguistics for digital health (telerehabilitation an rehabilitation medicines). Read more: [Letter to the Editor–Update from Ukraine: Development of the Cloud-based Platform for Patient-centered Telerehabilitation of Oncology Patients with Mathematical-related Modeling](https://doi.org/10.5195/ijt.2023.6562).

## Inspired by

This project was inspired by the original [privateGPT](https://github.com/imartinez/privateGPT) and [localGPT](https://github.com/PromtEngineer/localGPT).

Built with [LangChain](https://github.com/hwchase17/langchain), [GPT4All](https://github.com/nomic-ai/gpt4all), [LlamaCpp](https://github.com/ggerganov/llama.cpp), [Chroma](https://www.trychroma.com/), [SentenceTransformers](https://www.sbert.net/), [InstructorEmbeddings](https://instructor-embedding.github.io/).

## Sponsor this project

Please support @malakhovks. Despite the Wartime in Ukraine, R&D in the field of Digital Health are being resumed.
[https://send.monobank.ua/jar/5ad56oNAcD](https://send.monobank.ua/jar/5ad56oNAcD)

## Important note

**medlocalgpt** project and documentation are in active development. For any technical clarifications and questions contact me via email: [malakhovks@nas.gov.ua](mailto:malakhovks@nas.gov.ua) or via Issues. The recent Russian's rocket shelling on critical infrastructure in Ukraine and Kyiv led our server infrastructure to become unstable.
**CPU support only (for now)**

## 💻 Installation (Testing)

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
conda create -n medlocalgpt
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

```bash
export OPENAI_API_KEY="YOUR KEY"
```

```bash
export OPENAI_ORGANIZATION="YOUR ID"
```

6. Put all of your documents (.txt, .pdf, or .csv) into the SOURCE_DOCUMENTS and ingest all the data

```bash
python ingest.py
```

**CPU USAGE CAUTION**

First of you need a lot of CPU cores to processing (to ingest) more documents. The week point here is not a RAM size.
Also the **week point is the memory bandwidth**. That's why all this stuff working great on M1 or M2 chip.
Read more about that you can here: [How is LLaMa.cpp possible?](https://finbarr.ca/how-is-llama-cpp-possible/)

**PS:**  I also have a couple of HP servers, and using 28 cores, 1000 PDFs processed about 6 hours.

**Default models**

- Embedding model: `hkunlp/instructor-large` from [InstructorEmbeddings](https://instructor-embedding.github.io/)
- LLM: `orca-mini-3b.ggmlv3.q4_0.bin` from [TheBloke/orca_mini_3B-GGML](https://huggingface.co/TheBloke/orca_mini_3B-GGML)

Now you can set models via `model_property.py`.

7. Run medlocalgpt service

```bash
python run_server.py
```


## 💻 Installation (Production)

TODO

## 🎈 API usage

TODO

## 🗃️ Dataset

EBSCO articles dataset (domain knowledge: rehabilitation medicine)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8185659.svg)](https://doi.org/10.5281/zenodo.8185659)

```bash
wget -O ./ebsco-rehabilitation-dataset.zip https://cdn.e-rehab.pp.ua/u/ebsco-rehabilitation-dataset.zip
```
