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
    MAX_TOKENS_FOR_TRANSLATION = 3024

if 'DOC_NUMBER' in os.environ:
    DOC_NUMBER = os.environ['DOC_NUMBER']
else:
    DOC_NUMBER = 6

if 'SUBJECT' in os.environ:
    SUBJECT = os.environ['SUBJECT']
else:
    SUBJECT = "medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, health informatics, digital health, computer sciences, transdisciplinary research"

if 'MODEL' in os.environ:
    MODEL = os.environ['MODEL']
else:
    MODEL = "openai"

if 'TEMPERATURE' in os.environ:
    TEMPERATURE = os.environ['TEMPERATURE']
else:
    TEMPERATURE = 0.5

# from langchain.embeddings import HuggingFaceInstructEmbeddings
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Define the folder for storing database
SOURCE_DIRECTORY = f"{ROOT_DIRECTORY}/SOURCE_DOCUMENTS"

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

# DOCUMENT_MAP = {
#     ".txt": TextLoader,
#     ".md": TextLoader,
#     ".py": TextLoader,
#     ".pdf": PDFMinerLoader,
#     ".csv": CSVLoader,
#     ".xls": UnstructuredExcelLoader,
#     ".xlsx": UnstructuredExcelLoader,
#     ".docx": Docx2txtLoader,
#     ".doc": Docx2txtLoader,
# }

# Can be changed to a specific number
INGEST_THREADS = os.cpu_count()

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

Question: {question}
Answer:
"""
