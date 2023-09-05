import os

if 'OPENAI_API_KEY' in os.environ:
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
else:
    OPENAI_API_KEY = None

if 'OPENAI_ORGANIZATION' in os.environ:
    OPENAI_ORGANIZATION = os.environ['OPENAI_ORGANIZATION']
else:
    OPENAI_ORGANIZATION = None

if 'OPENAI_MODEL' in os.environ:
    OPENAI_MODEL = os.environ['OPENAI_MODEL']
else:
    OPENAI_MODEL="gpt-3.5-turbo-16k"

if 'EMBEDDING_MODEL_NAME' in os.environ:
    EMBEDDING_MODEL_NAME = os.environ['EMBEDDING_MODEL_NAME']
else:
    EMBEDDING_MODEL_NAME = "hkunlp/instructor-base"

if 'MODEL_ID' in os.environ:
    MODEL_ID = os.environ['MODEL_ID']
else:
    MODEL_ID = "TheBloke/orca_mini_3B-GGML"

if 'MODEL_BASENAME' in os.environ:
    MODEL_BASENAME = os.environ['MODEL_BASENAME']
else:
    MODEL_BASENAME = "orca-mini-3b.ggmlv3.q4_0.bin"

if 'DEVICE_TYPE' in os.environ:
    DEVICE_TYPE = os.environ['DEVICE_TYPE']
else:
    DEVICE_TYPE = "cpu"

if 'MAX_TOKENS' in os.environ:
    MAX_TOKENS = os.environ['MAX_TOKENS']
else:
    MAX_TOKENS = 1024

if 'MAX_TOKENS_OPENAI' in os.environ:
    MAX_TOKENS_OPENAI = os.environ['MAX_TOKENS']
else:
    MAX_TOKENS_OPENAI = 5024

if 'MAX_TOKENS_FOR_TRANSLATION' in os.environ:
    MAX_TOKENS_FOR_TRANSLATION = os.environ['MAX_TOKENS']
else:
    MAX_TOKENS_FOR_TRANSLATION = 5024

if 'DOC_NUMBER' in os.environ:
    DOC_NUMBER = os.environ['DOC_NUMBER']
else:
    DOC_NUMBER = 6

if 'SUBJECT' in os.environ:
    SUBJECT = os.environ['SUBJECT']
else:
    SUBJECT = "medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research"

if 'MODEL' in os.environ:
    MODEL = os.environ['MODEL']
else:
    MODEL = "openai"

if 'TEMPERATURE' in os.environ:
    TEMPERATURE = os.environ['TEMPERATURE']
else:
    TEMPERATURE = 0.5

# import torch
# from auto_gptq import AutoGPTQForCausalLM
# from huggingface_hub import hf_hub_download
# from langchain.embeddings import HuggingFaceInstructEmbeddings
# # from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.llms import HuggingFacePipeline, LlamaCpp

from chromadb.config import Settings

# https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/excel.html?highlight=xlsx#microsoft-excel
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader

# from langchain.embeddings import HuggingFaceInstructEmbeddings
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Define the folder for storing database
SOURCE_DIRECTORY = f"{ROOT_DIRECTORY}/SOURCE_DOCUMENTS"

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

# Can be changed to a specific number
INGEST_THREADS = os.cpu_count()

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIRECTORY, anonymized_telemetry=False
)

# https://python.langchain.com/en/latest/_modules/langchain/document_loaders/excel.html#UnstructuredExcelLoader
DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".md": TextLoader,
    ".py": TextLoader,
    ".pdf": PDFMinerLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}

# DEVICE_TYPE = "cpu"
# EMBEDDING_MODEL_NAME = "hkunlp/instructor-large"
# EMBEDDING_MODEL_NAME = "hkunlp/instructor-xl"
# EMBEDDING_MODEL_NAME = "hkunlp/instructor-base"
# EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

####
#### OTHER EMBEDDING MODEL OPTIONS
####

# EMBEDDING_MODEL_NAME = "hkunlp/instructor-xl" # Uses 5 GB of VRAM (Most Accurate of all models)
# EMBEDDING_MODEL_NAME = "intfloat/e5-large-v2" # Uses 1.5 GB of VRAM (A little less accurate than instructor-large)
# EMBEDDING_MODEL_NAME = "intfloat/e5-base-v2" # Uses 0.5 GB of VRAM (A good model for lower VRAM GPUs)
# EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # Uses 0.2 GB of VRAM (Less accurate but fastest - only requires 150mb of vram)

####
#### MULTILINGUAL EMBEDDING MODELS
####

# EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large" # Uses 2.5 GB of VRAM 
# EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-base" # Uses 1.2 GB of VRAM 

# EMBEDDINGS = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": DEVICE_TYPE})

#### SELECT AN OPEN SOURCE LLM (LARGE LANGUAGE MODEL)
    # Select the Model ID and model_basename
    # load the LLM for generating Natural Language responses

#### GPU VRAM Memory required for LLM Models (ONLY) by Billion Parameter value (B Model)
#### Does not include VRAM used by Embedding Models - which use an additional 2GB-7GB of VRAM depending on the model.
####
#### (B Model)   (float32)    (float16)    (GPTQ 8bit)         (GPTQ 4bit)
####    7b         28 GB        14 GB       7 GB - 9 GB        3.5 GB - 5 GB     
####    13b        52 GB        26 GB       13 GB - 15 GB      6.5 GB - 8 GB    
####    32b        130 GB       65 GB       32.5 GB - 35 GB    16.25 GB - 19 GB  
####    65b        260.8 GB     130.4 GB    65.2 GB - 67 GB    32.6 GB -  - 35 GB

# Select the Model ID and model_basename
# load the LLM for generating Natural Language responses
# MODEL_ID = "TheBloke/Llama-2-7B-Chat-GGML"
# MODEL_BASENAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"
# MODEL_ID = "TheBloke/orca_mini_3B-GGML"
# MODEL_BASENAME = "orca-mini-3b.ggmlv3.q4_0.bin"

# MODEL_ID = "TheBloke/vicuna-7B-v1.5-GGML"
# MODEL_BASENAME = "vicuna-7b-v1.5.ggmlv3.q4_1.bin"

# MODEL_ID = "TheBloke/orca_mini_v3_7B-GGML"
# MODEL_BASENAME = "orca_mini_v3_7b.ggmlv3.q4_0.bin"

# for HF models
# MODEL_ID = "TheBloke/vicuna-7B-1.1-HF"
# MODEL_BASENAME = None
# MODEL_ID = "TheBloke/Wizard-Vicuna-7B-Uncensored-HF"
# MODEL_ID = "TheBloke/guanaco-7B-HF"
# MODEL_ID = 'NousResearch/Nous-Hermes-13b' # Requires ~ 23GB VRAM. Using STransformers
# alongside will 100% create OOM on 24GB cards.
# llm = load_model(device_type, model_id=model_id)

# for GPTQ (quantized) models
# MODEL_ID = "TheBloke/Nous-Hermes-13B-GPTQ"
# MODEL_BASENAME = "nous-hermes-13b-GPTQ-4bit-128g.no-act.order"
# MODEL_ID = "TheBloke/WizardLM-30B-Uncensored-GPTQ"
# MODEL_BASENAME = "WizardLM-30B-Uncensored-GPTQ-4bit.act-order.safetensors" # Requires
# ~21GB VRAM. Using STransformers alongside can potentially create OOM on 24GB cards.
# MODEL_ID = "TheBloke/wizardLM-7B-GPTQ"
# MODEL_BASENAME = "wizardLM-7B-GPTQ-4bit.compat.no-act-order.safetensors"
# MODEL_ID = "TheBloke/WizardLM-7B-uncensored-GPTQ"
# MODEL_BASENAME = "WizardLM-7B-uncensored-GPTQ-4bit-128g.compat.no-act-order.safetensors"

# for GGML (quantized cpu+gpu+mps) models - check if they support llama.cpp
# MODEL_ID = "TheBloke/wizard-vicuna-13B-GGML"
# MODEL_BASENAME = "wizard-vicuna-13B.ggmlv3.q4_0.bin"
# MODEL_BASENAME = "wizard-vicuna-13B.ggmlv3.q6_K.bin"
# MODEL_BASENAME = "wizard-vicuna-13B.ggmlv3.q2_K.bin"
# MODEL_ID = "TheBloke/orca_mini_3B-GGML"
# MODEL_BASENAME = "orca-mini-3b.ggmlv3.q4_0.bin"

SYSTEM_TEMPLATE_FOR_TRANSLATION = """I want you to act as an translator, spelling and grammar corrector. \
            You will provided with the sample text. \
            Your task is to correct spelling and grammar mistakes using domain knowledge from: {subject} \
            Next step of your task is to translate the sample text from {input_lang} into {output_lang} language using domain knowledge from: {subject}. \
            Sample text: {sample_text} \
            Translation:
            """

SYSTEM_TEMPLATE_BASIC = """I want you to act as an AI assistant for healthcare professionals \
Correct spelling and grammar mistakes of the user question using domain knowledge from {subject}: {question} \
Do not include corrected version of user's question in your response. \
The subject areas of your responses should be: {subject}. \
The domain of your responses should be academic. \
Your responses should be logical. \
Your responses should be for knowledgeable and expert audience. \
If the question is not about {subject} and not directly in the given context, politely inform them that you are tuned to only answer questions about {subject}. \
If the question is not directly in the given context, just say that context do not provide this information \
Use only the following context to answer the question: \

{context}

Chat History:
{history}
Question: {question}
Answer:
"""

SYSTEM_TEMPLATE_ADVANCED_EN = """I want you to act as an AI assistant for healthcare professionals in {subject}
Correct spelling and grammar mistakes of the User question using domain knowledge from {subject}: {question} \
Do not include corrected version of User's question in your response. \
The subject areas of your responses should be: {subject}. \
The domain of your responses should be academic. \
Provide a very detailed comprehensive academic answer. \
Your responses should be informative and logical. \
Your responses should be for knowledgeable and expert audience. \
If the question is not about {subject}, politely inform User that you are tuned to only answer questions about {subject}. \

Chat History:
{history}
Question: {question}
Answer:
"""

# SYSTEM_TEMPLATE_BASIC_ADVANCED = """I want you to act as an AI assistant in {subject}
# Correct spelling and grammar mistakes of the user question using domain knowledge from {subject}: {question} \
# Do not include corrected version of user's question in your response. \
# The subject areas of your responses should be: {subject}. \
# The domain of your responses should be academic. \
# Provide a very detailed comprehensive academic answer. \
# Your responses should be informative and logical. \
# Your responses should be for knowledgeable and expert audience. \
# If you don't know the answer, just say that you don't know, don't try to make up an answer. \
# If the question is not about {subject} and not directly in the given context, politely inform them that you are tuned to only answer questions about {subject}. \
# If the question is not directly in the given context, just say that context do not provide this information \
# Use only the following context to answer the question: \

# {context}

# Chat History:
# {history}
# Question: {question}
# Answer:
# """
