import logging, os

os.environ["no_proxy"] = "*"

__author__ = "Kyrylo Malakhov <malakhovks@nas.gov.ua>"
__copyright__ = "Copyright (C) 2023 Kyrylo Malakhov <malakhovks@nas.gov.ua>"

from flask import Flask, jsonify, request, render_template
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain, SimpleSequentialChain

from model_property import (
    MODEL,
    OPENAI_API_KEY,
    OPENAI_ORGANIZATION,
    TEMPERATURE,
    OPENAI_MODEL,
    SUBJECT,
    SYSTEM_TEMPLATE_ADVANCED_EN,
    MAX_TOKENS)

PLATFORM = "OpenAI PLATFORM"
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logging.info(f"Running on: {PLATFORM}")

if MODEL == 'OpenAI':
    if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
        OPENAI_CHAT = ChatOpenAI(model_name=OPENAI_MODEL, max_tokens=int(MAX_TOKENS), openai_api_key=OPENAI_API_KEY, openai_organization=OPENAI_ORGANIZATION, temperature=TEMPERATURE)
        LLM_OPENAI_TR = ChatOpenAI(model_name=OPENAI_MODEL, max_tokens=int(MAX_TOKENS), openai_api_key=OPENAI_API_KEY, openai_organization=OPENAI_ORGANIZATION, temperature=TEMPERATURE)

app = Flask(__name__)

"""
Set the secret key to some random bytes. Keep this really secret!
How to generate good secret keys.
A secret key should be as random as possible. Your operating system has ways to generate pretty random data based on a cryptographic random generator. Use the following command to quickly generate a value for Flask.secret_key (or SECRET_KEY):
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
"""
app.secret_key = os.urandom(42)

# Tuning prompt (with selected domain knowledge) for query to OpenAI model in English
@app.route("/medlocalgpt/api/v1/en/advanced/openai/ask", methods=["GET", "POST"])
def process_en_advanced_openai_query_v1():
    # user_prompt = request.form.get("prompt")
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        request_json = request.get_json()
        user_prompt = request_json.get('prompt')
    else:
        return 'Content-Type not supported!', 400

    if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
        logging.debug(f"Use LLM_OPENAI")
    else:
        return "No OPENAI cridentials received", 400

    if user_prompt:
        logging.debug(f"Get the answer from the chain")

        system_message_prompt = SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE_ADVANCED_EN)
        human_template = "{question}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
                    [system_message_prompt, human_message_prompt]
        )
        # initialize LLMChain by passing LLM and prompt template
        # res = OPENAI_CHAT(
        #     chat_prompt.format_prompt(
        #         question=user_prompt, subject=SUBJECT
        #     ).to_messages()
        # )
        chain = LLMChain(llm=OPENAI_CHAT, prompt=chat_prompt)
        res = chain.run(question=user_prompt, subject=SUBJECT)
        # llm_chain = LLMChain(llm=OPENAI_CHAT, prompt=chat_prompt_template)
        # res = llm_chain.run(question=user_prompt, subject=SUBJECT)

        logging.debug(f"RESULTS: {res}")

        return jsonify({"response": res, "prompt": user_prompt}), 200
    else:
        return "No user prompt received", 400

@app.route("/medlocalgpt/api/v1/uk/advanced/openai/ask", methods=["GET", "POST"])
def process_uk_advanced_openai_query_v1():
    # user_prompt = request.form.get("prompt")
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        request_json = request.get_json()
        user_prompt = request_json.get('prompt')
    else:
        return 'Content-Type not supported!', 400

    if OPENAI_API_KEY and OPENAI_ORGANIZATION is not None:
        logging.debug(f"Use LLM_OPENAI")
    else:
        return "No OPENAI cridentials received", 400

    if user_prompt:
        logging.debug(f"Get the answer from the chain")

        # This is an LLMChain to translate text -----------------------------------------------------------------------------
        translate_template = """I want you to act as an translator, spelling and grammar corrector. \
            You will provided with the sample text. \
            Your task is to correct spelling and grammar mistakes using domain knowledge from: medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research. \
            Next step of your task is to translate the sample text from Ukrainian into English language using domain knowledge from: medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research. \
            Sample text: {sample_text} \
            Translation:
            """
        system_prompt_translate_template = SystemMessagePromptTemplate.from_template(translate_template)
        human_translate_template = "{sample_text}"
        human_prompt_translate_template = HumanMessagePromptTemplate.from_template(human_translate_template)
        chat_prompt_translate_template = ChatPromptTemplate.from_messages(
                    [system_prompt_translate_template, human_prompt_translate_template]
                )
        llm_chain_1 = LLMChain(
            llm=LLM_OPENAI_TR,
            prompt=chat_prompt_translate_template
            )
         # This is an LLMChain to ask question -----------------------------------------------------------------------------
        ask_template = """I want you to act as an AI assistant for healthcare professionals in medicine, physical rehabilitation medicine, telerehabilitation, breast canser, cardiovascular system, arterial oscillography, telemedicine, health informatics, digital health, computer sciences, transdisciplinary research. \
        Correct spelling and grammar mistakes of the User question using domain knowledge from medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research: {translated_question} \
        Do not include corrected version of User's question in your response. \
        The subject areas of your responses should be: medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, health informatics, digital health, computer sciences, transdisciplinary research. \
        The domain of your responses should be academic. \
        Provide a detailed comprehensive academic answer. \
        Your responses should be logical. \
        Your responses should be for knowledgeable and expert audience. \
        Limit your response up to 1024 completion_tokens. \
        If the question is not about medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research, politely inform User that you are tuned to only answer questions about medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research. \
        Question: {translated_question}
        Answer:
        """
        system_prompt_ask_template = PromptTemplate.from_template(ask_template)
        llm_chain_2 = LLMChain(
            llm=LLM_OPENAI_TR,
            prompt=system_prompt_ask_template
            )

        # This is an LLMChain to translate text -----------------------------------------------------------------------------
        translate_template_2 = """I want you to act as an translator, spelling and grammar corrector. \
            You will provided with the sample text. \
            Your task is to correct spelling and grammar mistakes using domain knowledge from: medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research. \
            Next step of your task is to translate the sample text from English into Ukrainian language using domain knowledge from: medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, arterial oscillography, health informatics, digital health, computer sciences, transdisciplinary research. \
            Sample text: {sample_text} \
            Translation:
            """
        system_prompt_translate_template = SystemMessagePromptTemplate.from_template(translate_template_2)
        human_prompt_translate_template = HumanMessagePromptTemplate.from_template(human_translate_template)
        chat_prompt_translate_template_2 = ChatPromptTemplate.from_messages(
                    [system_prompt_translate_template, human_prompt_translate_template]
                )
        llm_chain_3 = LLMChain(
            llm=LLM_OPENAI_TR,
            prompt=chat_prompt_translate_template_2
            )
        overall_chain = SimpleSequentialChain(chains=[llm_chain_1, llm_chain_2, llm_chain_3], verbose=True)
        output = overall_chain.run(user_prompt)

        return jsonify({"response": output, "prompt": user_prompt}), 200
    else:
        return "No user prompt received", 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)