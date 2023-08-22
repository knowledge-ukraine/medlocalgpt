# medlocalgpt

Ask your (medical) dataset privately using LLMs and Embeddings. No data leaves your infrastructure/platform and 100% private.
Optionally you can use OpenAI GPT models or other LLM SaaS solutions.

This project is part of the R&D on intelligent data analysis and computational linguistics for digital health (telerehabilitation an rehabilitation medicine). Read more: [Letter to the Editor–Update from Ukraine: Development of the Cloud-based Platform for Patient-centered Telerehabilitation of Oncology Patients with Mathematical-related Modeling](https://doi.org/10.5195/ijt.2023.6562).

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

TODO

## 💻 Installation (Production)

TODO

## 🗃️ Dataset

EBSCO articles dataset (domain knowledge: rehabilitation medicine)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8185659.svg)](https://doi.org/10.5281/zenodo.8185659)

```bash
wget -O ./ebsco-rehabilitation-dataset.zip https://cdn.e-rehab.pp.ua/u/ebsco-rehabilitation-dataset.zip
```
