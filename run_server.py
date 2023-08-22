import logging
import os, json, re
import shutil
import subprocess

# import torch
from auto_gptq import AutoGPTQForCausalLM
from huggingface_hub import hf_hub_download
from flask import Flask, jsonify, request
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline, LlamaCpp
from langchain.llms import OpenAI


# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
    pipeline,
)
from werkzeug.utils import secure_filename

from constants import (
    CHROMA_SETTINGS,
    PERSIST_DIRECTORY,
    LLM_LOCAL,
    LLM_OPENAI,
    EMBEDDINGS)

from googletrans import Translator

DEVICE_TYPE = "cpu"
SHOW_SOURCES = True
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logging.info(f"Running on: {DEVICE_TYPE}")
logging.info(f"Display Source Documents set to: {SHOW_SOURCES}")

DB = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=EMBEDDINGS,
    client_settings=CHROMA_SETTINGS,
)

RETRIEVER = DB.as_retriever(search_kwargs={"k": 5})

QA_LOCAL = RetrievalQA.from_chain_type(
    llm=LLM_LOCAL, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES
)

QA_OPENAI = RetrievalQA.from_chain_type(
    llm=LLM_OPENAI, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES
)

app = Flask(__name__)

"""
Set the secret key to some random bytes. Keep this really secret!
How to generate good secret keys.
A secret key should be as random as possible. Your operating system has ways to generate pretty random data based on a cryptographic random generator. Use the following command to quickly generate a value for Flask.secret_key (or SECRET_KEY):
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
"""
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.secret_key = os.urandom(42)

@app.route("/medlocalgpt/api/v1/delete_source", methods=["GET"])
def delete_source_route():
    folder_name = "SOURCE_DOCUMENTS"

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.makedirs(folder_name)

    return jsonify({"message": f"Folder '{folder_name}' successfully deleted and recreated."})

# add route to delete PERSIST_DIRECTORY

@app.route("/medlocalgpt/api/v1/save_document", methods=["GET", "POST"])
def save_document_route():
    if "document" not in request.files:
        return "No document part", 400
    file = request.files["document"]
    if file.filename == "":
        return "No selected file", 400
    if file:
        filename = secure_filename(file.filename)
        folder_path = "SOURCE_DOCUMENTS"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, filename)
        file.save(file_path)
        return "File saved successfully", 200


@app.route("/medlocalgpt/api/v1/ingest", methods=["GET"])
def run_ingest_route():
    global DB
    global RETRIEVER
    global QA

    try:
        if os.path.exists(PERSIST_DIRECTORY):
            try:
                shutil.rmtree(PERSIST_DIRECTORY)
            except OSError as e:
                logging.error(f"Error: {e.filename} - {e.strerror}.")
        else:
            logging.info(PERSIST_DIRECTORY + " directory does not exist")

        run_langest_commands = ["python", "ingest.py"]
        if DEVICE_TYPE == "cpu":
            run_langest_commands.append("--device_type")
            run_langest_commands.append(DEVICE_TYPE)
            
        result = subprocess.run(run_langest_commands, capture_output=True)
        if result.returncode != 0:
            return "Script execution failed: {}".format(result.stderr.decode("utf-8")), 500
        # load the vectorstore
        DB = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=EMBEDDINGS,
            client_settings=CHROMA_SETTINGS,
        )
        RETRIEVER = DB.as_retriever(5)

        QA = RetrievalQA.from_chain_type(
            llm=LLM_LOCAL, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES
        )
        return "Script executed successfully: {}".format(result.stdout.decode("utf-8")), 200
    except Exception as e:
        return f"Error occurred: {str(e)}", 500


@app.route("/medlocalgpt/api/v1/ask", methods=["GET", "POST"])
def prompt_route():
    # global QA

    #  template = """You are an AI assistant for answering questions about {subject}. Provide a very detailed comprehensive academic answer. If you don't know the answer, just say "I'm not sure." Don't try to make up an answer. If the question is not about {subject} and not directly in the given context, politely inform them that you are tuned to only answer questions about {subject}. Question: {question} ========= {context} ========= Answer:"""

    use_model = request.args.get('model', default = 'local', type = str)

    if use_model == 'openai':
        QA = QA_OPENAI
        logging.debug('Use QA_OPENAI')
    if use_model == 'local':
        QA = QA_LOCAL
        logging.debug('Use QA_LOCAL')

    user_prompt = request.form.get("prompt")
    if user_prompt:
        # Get the answer from the chain
        logging.debug('Get the answer from the chain')
        res = QA(user_prompt)
        answer, docs = res["result"], res["source_documents"]

        prompt_response_dict = {
            "Prompt": user_prompt,
            "Answer": answer,
        }

        prompt_response_dict["Sources"] = []
        for document in docs:
            prompt_response_dict["Sources"].append(
                (os.path.basename(str(document.metadata["source"])), 'https://cdn.e-rehab.pp.ua/u/' + re.sub(r"\s+", '%20', os.path.basename(str(document.metadata["source"]))), str(document.page_content))
            )

        logging.debug('RESULTS:' + json.dumps(prompt_response_dict, indent=4))

        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 400

@app.route("/medlocalgpt/api/v1/gt/ask", methods=["GET", "POST"])
def prompt_gt():
    # global QA
    translator = Translator()

    #  template = """You are an AI assistant for answering questions about {subject}. Provide a very detailed comprehensive academic answer. If you don't know the answer, just say "I'm not sure." Don't try to make up an answer. If the question is not about {subject} and not directly in the given context, politely inform them that you are tuned to only answer questions about {subject}. Question: {question} ========= {context} ========= Answer:"""
    
    use_model = request.args.get('model', default = 'local', type = str)
    lang_src = request.args.get('lang_src', default = 'uk', type = str)
    lang_dest = request.args.get('lang_dest', default = 'en', type = str)

    if use_model == 'openai':
        logging.debug('Use QA_OPENAI')
        QA = QA_OPENAI
    if use_model == 'local':
        logging.debug('Use QA_LOCAL')
        QA = QA_LOCAL

    user_prompt = request.form.get("prompt")
    if user_prompt:
        #Translation uk to en
        # logging.info(translator.translate(user_prompt, src='uk', dest='en'))
        # tr_prompt = translator.translate(user_prompt, src='uk', dest='en')
        logging.debug('Translation from ' + lang_src + ' to ' + lang_dest)
        tr_prompt = translator.translate(user_prompt, src=lang_src, dest=lang_dest)
        # Get the answer from the chain
        logging.debug('Get the answer from the chain')
        res = QA(tr_prompt.text)
        answer, docs = res["result"], res["source_documents"]

        #Translation en to uk
        logging.debug('Translation from en to uk')
        tr_response = translator.translate(answer, src='en', dest='uk')

        prompt_response_dict = {
            "Prompt": user_prompt,
            "Answer": tr_response.text,
        }

        prompt_response_dict["Sources"] = []
        for document in docs:
            prompt_response_dict["Sources"].append(
                (os.path.basename(str(document.metadata["source"])), 'https://cdn.e-rehab.pp.ua/u/' + re.sub(r"\s+", '%20', os.path.basename(str(document.metadata["source"]))), str(document.page_content))
            )

        logging.debug('RESULTS:' + json.dumps(prompt_response_dict, indent=4))

        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
