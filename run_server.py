import logging
import os, json
import shutil
import subprocess

import torch
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

from constants import CHROMA_SETTINGS, EMBEDDING_MODEL_NAME, PERSIST_DIRECTORY, MODEL_ID, MODEL_BASENAME

from googletrans import Translator

DEVICE_TYPE = "cpu"
SHOW_SOURCES = True
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logging.info(f"Running on: {DEVICE_TYPE}")
logging.info(f"Display Source Documents set to: {SHOW_SOURCES}")

EMBEDDINGS = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": DEVICE_TYPE})

def load_model(device_type, model_id, model_basename=None):
    logging.info(f"Loading Model: {model_id}, on: {device_type}")
    logging.info("This action can take a few minutes!")

    if model_basename is not None:
        if ".ggml" in model_basename:
            logging.info("Using Llamacpp for GGML quantized models")
            model_path = hf_hub_download(repo_id=model_id, filename=model_basename)
            max_ctx_size = 2048
            kwargs = {
                "model_path": model_path,
                "n_ctx": max_ctx_size,
                "max_tokens": max_ctx_size,
            }
            if device_type.lower() == "mps":
                kwargs["n_gpu_layers"] = 1000
            if device_type.lower() == "cuda":
                kwargs["n_gpu_layers"] = 1000
                kwargs["n_batch"] = max_ctx_size
            return LlamaCpp(**kwargs)

        else:
            # The code supports all huggingface models that ends with GPTQ and have some variation
            # of .no-act.order or .safetensors in their HF repo.
            logging.info("Using AutoGPTQForCausalLM for quantized models")

            if ".safetensors" in model_basename:
                # Remove the ".safetensors" ending if present
                model_basename = model_basename.replace(".safetensors", "")

            tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
            logging.info("Tokenizer loaded")

            model = AutoGPTQForCausalLM.from_quantized(
                model_id,
                model_basename=model_basename,
                use_safetensors=True,
                trust_remote_code=True,
                device="cuda:0",
                use_triton=False,
                quantize_config=None,
            )
    elif (
        device_type.lower() == "cuda"
    ):  # The code supports all huggingface models that ends with -HF or which have a .bin
        # file in their HF repo.
        logging.info("Using AutoModelForCausalLM for full models")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        logging.info("Tokenizer loaded")

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            # max_memory={0: "15GB"} # Uncomment this line with you encounter CUDA out of memory errors
        )
        model.tie_weights()
    else:
        logging.info("Using LlamaTokenizer")
        tokenizer = LlamaTokenizer.from_pretrained(model_id)
        model = LlamaForCausalLM.from_pretrained(model_id)

    # Load configuration from the model to avoid warnings
    generation_config = GenerationConfig.from_pretrained(model_id)
    # see here for details:
    # https://huggingface.co/docs/transformers/
    # main_classes/text_generation#transformers.GenerationConfig.from_pretrained.returns

    # Create a pipeline for text generation
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=2048,
        temperature=0,
        top_p=0.95,
        repetition_penalty=1.15,
        generation_config=generation_config,
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)
    logging.info("Local LLM Loaded")

    return local_llm

DB = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=EMBEDDINGS,
    client_settings=CHROMA_SETTINGS,
)

RETRIEVER = DB.as_retriever(search_kwargs={"k": 5})

LLM_LOCAL = load_model(device_type=DEVICE_TYPE, model_id=MODEL_ID, model_basename=MODEL_BASENAME)
LLM_OPENAI = OpenAI(openai_api_key=" ", openai_organization=" ")

QA = RetrievalQA.from_chain_type(
    llm=LLM_LOCAL, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES
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


@app.route("/medlocalgpt/api/v1/run_ingest", methods=["GET"])
def run_ingest_route():
    global DB
    global RETRIEVER
    global QA
    try:
        if os.path.exists(PERSIST_DIRECTORY):
            try:
                shutil.rmtree(PERSIST_DIRECTORY)
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")
        else:
            print("The directory does not exist")

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
    global QA

    #  template = """You are an AI assistant for answering questions about {subject}. Provide a very detailed comprehensive academic answer. If you don't know the answer, just say "I'm not sure." Don't try to make up an answer. If the question is not about {subject} and not directly in the given context, politely inform them that you are tuned to only answer questions about {subject}. Question: {question} ========= {context} ========= Answer:"""
    
    use_model = request.args.get('model', default = 'local', type = str)

    if use_model == 'openai':
        QA = RetrievalQA.from_chain_type(llm=LLM_OPENAI, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES)
    if use_model == 'local':
        QA = RetrievalQA.from_chain_type(llm=LLM_LOCAL, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES)

    user_prompt = request.form.get("prompt")
    if user_prompt:
        # print(f'User Prompt: {user_prompt}')
        # Get the answer from the chain
        res = QA(user_prompt)
        answer, docs = res["result"], res["source_documents"]

        prompt_response_dict = {
            "Prompt": user_prompt,
            "Answer": answer,
        }

        prompt_response_dict["Sources"] = []
        for document in docs:
            prompt_response_dict["Sources"].append(
                (os.path.basename(str(document.metadata["source"])), str(document.page_content))
            )

        logging.debug(json.dumps(prompt_response_dict, indent=4))

        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 400

@app.route("/medlocalgpt/api/v1/gt/uk-en/ask", methods=["GET", "POST"])
def prompt_uk_en():
    global QA
    translator = Translator()

    #  template = """You are an AI assistant for answering questions about {subject}. Provide a very detailed comprehensive academic answer. If you don't know the answer, just say "I'm not sure." Don't try to make up an answer. If the question is not about {subject} and not directly in the given context, politely inform them that you are tuned to only answer questions about {subject}. Question: {question} ========= {context} ========= Answer:"""
    
    use_model = request.args.get('model', default = 'local', type = str)

    if use_model == 'openai':
        QA = RetrievalQA.from_chain_type(llm=LLM_OPENAI, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES)
    if use_model == 'local':
        QA = RetrievalQA.from_chain_type(llm=LLM_LOCAL, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES)

    user_prompt = request.form.get("prompt")
    if user_prompt:
        #Translation uk to en
        # logging.info(translator.translate(user_prompt, src='uk', dest='en'))
        tr_prompt = translator.translate(user_prompt, src='uk', dest='en')
        # Get the answer from the chain
        res = QA(tr_prompt.text)
        answer, docs = res["result"], res["source_documents"]

        #Translation en to uk
        tr_response = translator.translate(answer, src='en', dest='uk')

        prompt_response_dict = {
            "Prompt": user_prompt,
            "Answer": tr_response.text,
        }

        prompt_response_dict["Sources"] = []
        for document in docs:
            prompt_response_dict["Sources"].append(
                (os.path.basename(str(document.metadata["source"])), str(document.page_content))
            )

        logging.debug(json.dumps(prompt_response_dict, indent=4))

        return jsonify(prompt_response_dict), 200
    else:
        return "No user prompt received", 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
