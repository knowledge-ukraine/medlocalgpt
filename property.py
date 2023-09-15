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

if 'MAX_TOKENS' in os.environ:
    MAX_TOKENS = os.environ['MAX_TOKENS']
else:
    MAX_TOKENS = 1024

if 'MAX_TOKENS_OPENAI' in os.environ:
    MAX_TOKENS_OPENAI = os.environ['MAX_TOKENS_OPENAI']
else:
    MAX_TOKENS_OPENAI = 3024

if 'MAX_TOKENS_FOR_TRANSLATION' in os.environ:
    MAX_TOKENS_FOR_TRANSLATION = os.environ['MAX_TOKENS_FOR_TRANSLATION']
else:
    MAX_TOKENS_FOR_TRANSLATION = 3024

if 'SUBJECT' in os.environ:
    SUBJECT = os.environ['SUBJECT']
else:
    SUBJECT = "medicine, physical rehabilitation medicine, telerehabilitation, cardiovascular system, health informatics, digital health, computer sciences, transdisciplinary research"

if 'SUBJECT_UK' in os.environ:
    SUBJECT_UK = os.environ['SUBJECT_UK']
else:
    SUBJECT_UK = "медицина, фізична реабілітаційна медицина, телереабілітація, рак молочної залози, серцево-судинна система, медична інформатика, телемедицина, цифрова медицина, комп'ютерні науки, трансдисциплінарні дослідження"

if 'MODEL' in os.environ:
    MODEL = os.environ['MODEL']
else:
    MODEL = "openai"

if 'TEMPERATURE' in os.environ:
    TEMPERATURE = os.environ['TEMPERATURE']
else:
    TEMPERATURE = 0.5

SYSTEM_TEMPLATE_FOR_TRANSLATION = """I want you to act as an translator, spelling and grammar corrector. \
            You will provided with the sample text. \
            Your task is to correct spelling and grammar mistakes using domain knowledge from: {subject} \
            Next step of your task is to translate the sample text from {input_lang} into {output_lang} language using domain knowledge from: {subject}. \
            Sample text: {sample_text} \
            Translation:
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

SYSTEM_TEMPLATE_ADVANCED_UK = """Я хочу, щоб ви діяли як ШІ-асистент для медичних працівників (лікарів, реабілітологів) у галузях: {subject} \
Виправте орфографічні та граматичні помилки у запитанні користувача, використовуючи предметні галузі {subject}: {question} \
Не включайте виправлену версію запитання користувача у свою відповідь. \
Предметні галузі ваших відповідей повинні бути: {subject}. \
Тематика ваших відповідей повинна бути академічною. \
Надайте дуже детальну всебічну академічну відповідь. \
Ваші відповіді повинні бути інформативними та логічними. \
Ваші відповіді повинні бути розраховані на досвідчену та експертну аудиторію. \
Обмежте відповідь до 3024 completion_tokens. \
Якщо питання не стосується газузей {subject}, ввічливо повідомте Користувачеві, що ви налаштовані відповідати лише на питання у галузях {subject}

Питання: {question}
Відповідь:
"""
