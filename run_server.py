import logging
import os, json, re
import shutil
import subprocess

os.environ["no_proxy"] = "*"

import torch
from auto_gptq import AutoGPTQForCausalLM
from huggingface_hub import hf_hub_download
from flask import Flask, jsonify, request
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline, LlamaCpp
# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain

from googletrans import Translator

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
    pipeline
)
from werkzeug.utils import secure_filename

from model_property import (
    CHROMA_SETTINGS,
    PERSIST_DIRECTORY,
    MODEL_ID,
    MODEL_BASENAME,
    OPENAI_API_KEY,
    OPENAI_ORGANIZATION,
    EMBEDDING_MODEL_NAME,
    MAX_TOKENS,
    OPENAI_MODEL,
    DOC_NUMBER,
    SUBJECT,
    SYSTEM_TEMPLATE_FOR_TRANSLATION,
    SYSTEM_TEMPLATE_BASIC)

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

    # Create a pipeline for text generation
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=MAX_TOKENS,
        temperature=0,
        top_p=0.95,
        repetition_penalty=1.15,
        generation_config=generation_config,
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)
    logging.info("Local LLM Loaded")

    return local_llm

DEVICE_TYPE = "cpu"
SHOW_SOURCES = True
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logging.info(f"Running on: {DEVICE_TYPE}")
logging.info(f"Display Source Documents set to: {SHOW_SOURCES}")

template = """Correct spelling and grammatical mistakes of the user question using domain knowledge from {subject}: {question} \
Do not include corrected version of user's question in your response. \
The subject areas of your responses should be: {subject}. \
The domain of your responses should be academic. \
Provide a very detailed comprehensive academic answer. \
Your responses should be informative and logical. \
Your responses should be for knowledgeable and expert audience. \
If you don't know the answer, just say that you don't know, don't try to make up an answer. \
If the question is not about {subject} and not directly in the given context, politely inform them that you are tuned to only answer questions about {subject}. \
If the question is not directly in the given pieces of context, just say that context do not provide this information \
Use the following pieces of context to answer the question. \

{context}

Chat History:
{history}
Question: {question}
Answer:"""

prompt = PromptTemplate(input_variables=["history", "context", "question", "subject"], template=template)
memory = ConversationBufferMemory(input_key="question", memory_key="history", return_messages=True)

EMBEDDINGS = HuggingFaceInstructEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": DEVICE_TYPE})
DB = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=EMBEDDINGS,
    client_settings=CHROMA_SETTINGS,
)
RETRIEVER = DB.as_retriever(search_kwargs={"k": int(DOC_NUMBER)})

LLM_LOCAL = load_model(device_type=DEVICE_TYPE, model_id=MODEL_ID, model_basename=MODEL_BASENAME)
QA_LOCAL = RetrievalQA.from_chain_type(
    llm=LLM_LOCAL, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES
)

if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
    LLM_OPENAI = ChatOpenAI(model=OPENAI_MODEL, max_tokens=int(MAX_TOKENS), openai_api_key=OPENAI_API_KEY, openai_organization=OPENAI_ORGANIZATION)
    LLM_OPENAI_TR = ChatOpenAI(model=OPENAI_MODEL, max_tokens=1024, openai_api_key=OPENAI_API_KEY, openai_organization=OPENAI_ORGANIZATION)
    QA_OPENAI = RetrievalQA.from_chain_type(
        llm=LLM_OPENAI, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES,
        chain_type_kwargs={"prompt": prompt.partial(subject=SUBJECT), "memory": memory}
        )

app = Flask(__name__)

"""
Set the secret key to some random bytes. Keep this really secret!
How to generate good secret keys.
A secret key should be as random as possible. Your operating system has ways to generate pretty random data based on a cryptographic random generator. Use the following command to quickly generate a value for Flask.secret_key (or SECRET_KEY):
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
"""
app.secret_key = os.urandom(42)

@app.route("/medlocalgpt/api/v1/delete_source", methods=["GET"])
def delete_source_route():
    folder_name = "SOURCE_DOCUMENTS"

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    os.makedirs(folder_name)

    return jsonify({"message": f"Folder '{folder_name}' successfully deleted and recreated."})

# add route to delete PERSIST_DIRECTORY

@app.route("/medlocalgpt/api/v1/admin/save_document", methods=["GET", "POST"])
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


@app.route("/medlocalgpt/api/v1/admin/ingest", methods=["GET"])
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


# @app.route("/medlocalgpt/api/v1/en/ask", methods=["GET", "POST"])
# def process_en_query():
#     use_model = request.args.get('model', default = 'local', type = str)
#     user_prompt = request.form.get("prompt")

#     if use_model == 'openai':
#         if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
#             qa = QA_OPENAI
#             logging.debug('Use QA_OPENAI')
#         else:
#             return "No OPENAI cridentials received", 400
#     if use_model == 'local':
#         qa = QA_LOCAL
#         logging.debug('Use QA_LOCAL')

#     if user_prompt:
#         logging.debug('Get the answer from the chain')

#         res = qa(user_prompt)
#         answer, docs = res["result"], res["source_documents"]

#         prompt_response_dict = {
#             "Prompt": user_prompt,
#             "Answer": answer,
#         }

#         prompt_response_dict["Sources"] = []
#         for document in docs:
#             prompt_response_dict["Sources"].append(
#                 (os.path.basename(str(document.metadata["source"])), 'https://cdn.e-rehab.pp.ua/u/' + re.sub(r"\s+", '%20', os.path.basename(str(document.metadata["source"]))), str(document.page_content))
#             )

#         logging.debug('RESULTS:' + json.dumps(prompt_response_dict, indent=4))

#         return jsonify(prompt_response_dict), 200
#     else:
#         return "No user prompt received", 400

@app.route("/medlocalgpt/api/v1/en/ask", methods=["GET", "POST"])
def process_en_query():
    use_model = request.args.get('model', default = 'local', type = str)
    user_prompt = request.form.get("prompt")

    if use_model == 'openai':
        if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
            system_message_prompt_template = SystemMessagePromptTemplate.from_template(
                    SYSTEM_TEMPLATE_BASIC
                )
            human_template = "{context}\n{question}"
            human_message_prompt_template = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt_template = ChatPromptTemplate.from_messages(
                    [system_message_prompt_template, human_message_prompt_template]
                )
            final_prompt = chat_prompt_template.format_prompt(subject=SUBJECT).to_messages()
            qa_openai = RetrievalQA.from_chain_type(
                    llm=LLM_OPENAI, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES,
                    chain_type_kwargs={"prompt": final_prompt, "memory": memory}
                )
            qa = qa_openai
            logging.debug('Use QA_OPENAI')
        else:
            return "No OPENAI cridentials received", 400
    if use_model == 'local':
        qa = QA_LOCAL
        logging.debug('Use QA_LOCAL')

    if user_prompt:
        logging.debug('Get the answer from the chain')

        res = qa(question=user_prompt)
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

@app.route("/medlocalgpt/api/v1/ask", methods=["GET", "POST"])
def prompt_route():
    # global QA

    use_model = request.args.get('model', default = 'local', type = str)
    user_prompt = request.form.get("prompt")
    lang_src = request.args.get('lang_src', default = 'Ukrainian', type = str)
    lang_dest = request.args.get('lang_dest', default = 'English', type = str)

    if use_model == 'openai':
        if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
            system_message_prompt_template = SystemMessagePromptTemplate.from_template(
                    SYSTEM_TEMPLATE_FOR_TRANSLATION
                )
            human_template = "{sample_text}"
            human_message_prompt_template = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt_template = ChatPromptTemplate.from_messages(
                    [system_message_prompt_template, human_message_prompt_template]
                )
            # initialize LLMChain by passing LLM and prompt template
            llm_chain_1 = LLMChain(llm=LLM_OPENAI, prompt=chat_prompt_template)

            qa_openai = RetrievalQA.from_chain_type(
                    llm=LLM_OPENAI, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES,
                    chain_type_kwargs={"prompt": prompt.partial(subject=SUBJECT), "memory": memory}
                )
            qa = qa_openai

            logging.debug('Use QA_OPENAI')
        else:
            return "No OPENAI cridentials received", 400
    if use_model == 'local':
        qa = QA_LOCAL
        logging.debug('Use QA_LOCAL')

    if user_prompt:
        logging.debug('Get the answer from the chain')

        tr = llm_chain_1.run(input_lang=lang_src, output_lang=lang_dest, subject=SUBJECT,sample_text=user_prompt)
        logging.debug(f"Translation Uk-En: {tr}")

        res = qa(tr)

        answer, docs = res["result"], res["source_documents"]

        tr = llm_chain_1.run(input_lang=lang_dest, output_lang=lang_src, subject=SUBJECT,sample_text=answer)

        logging.debug(f"Translation En-Uks: {tr}")

        prompt_response_dict = {
            "Prompt": user_prompt,
            "Answer": tr,
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

    use_model = request.args.get('model', default = 'local', type = str)
    lang_src = request.args.get('lang_src', default = 'uk', type = str)
    lang_dest = request.args.get('lang_dest', default = 'en', type = str)

    if use_model == 'openai':
        if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
            logging.debug('Use QA_OPENAI')
            qa_openai = RetrievalQA.from_chain_type(
                    llm=LLM_OPENAI, chain_type="stuff", retriever=RETRIEVER, return_source_documents=SHOW_SOURCES,
                    chain_type_kwargs={"prompt": prompt.partial(subject=SUBJECT), "memory": memory}
                )
            qa = qa_openai
        else:
            return "No OPENAI cridentials received", 400
    if use_model == 'local':
        logging.debug('Use QA_LOCAL')
        qa = QA_LOCAL

    user_prompt = request.form.get("prompt")
    if user_prompt:
        #Translation uk to en
        # logging.info(translator.translate(user_prompt, src='uk', dest='en'))
        # tr_prompt = translator.translate(user_prompt, src='uk', dest='en')
        logging.debug('Translation from ' + lang_src + ' to ' + lang_dest)
        tr_prompt = translator.translate(user_prompt, src=lang_src, dest=lang_dest)
        logging.debug('Get the answer from the chain')
        res = qa(tr_prompt.text)
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
