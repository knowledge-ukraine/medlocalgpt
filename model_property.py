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
    MAX_TOKENS = 3024

if 'SUBJECT' in os.environ:
    SUBJECT = os.environ['SUBJECT']
else:
    SUBJECT = "medicine, physical and rehabilitation medicine, telerehabilitation, cardiovascular system, health informatics, digital health, computer sciences, transdisciplinary research"

if 'SUBJECT_UA' in os.environ:
    SUBJECT_UA = os.environ['SUBJECT']
else:
    SUBJECT_UA = "медицина, фізична та реабілітаційна медицина, телереабілітація, рак молочної залози, медична інформатика, цифрова медицина, комп'ютерні науки, трансдисциплінарні дослідження"

if 'MODEL' in os.environ:
    MODEL = os.environ['MODEL']
else:
    MODEL = "OpenAI"

if 'TEMPERATURE' in os.environ:
    TEMPERATURE = os.environ['TEMPERATURE']
else:
    TEMPERATURE = 0.5

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

SYSTEM_TEMPLATE_ADVANCED_UA = """Я хочу, щоб ви діяли як ШІ-асистент для медичних працівників у галузі охорони здоров'я, а саме: {subject}.
Виправте орфографічні та граматичні помилки у запитанні користувача (використовуючи знання з предметних галузей: {subject}): {question} \
Не включайте виправлену редакцію запитання користувача у свою відповідь. \
Предметні галузі ваших відповідей повинні включати в себе: {subject}. \
Домен ваших відповідей повинен бути академічним. \
Надайте детальну та всебічну академічну відповідь. \
Ваші відповіді повинні бути інформативними та логічними. \
Ваші відповіді повинні бути розраховані на обізнану та експертну аудиторію. \
Якщо питання не стосується {subject}, ввічливо повідомте Користувачеві, що ви налаштовані відповідати лише на питання з {subject}.

Питання: {question}
Відповідь:
"""
