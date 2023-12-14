import website.parameters as parameters
import asyncio
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from website import app, mail
from openai import OpenAI

client = OpenAI(
  api_key = parameters.openAISecret,
)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def requestChatGPT(text):
    try:
        main_text = "Del siguiente texto extraer la lista de ingredientes solamente, la lista debe estar en formato CSV, el sepador será '++', cada ingrediente debe estar en mayuscula fija. Si no es posible encontrar ingredientes retorna solamente la palabra VACÍO. El texto es :"
        result = f"{main_text}\n{text}"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": result,
                }
            ],
            model="gpt-3.5-turbo",
        )
    except ValueError as e:
        print(e)
        return "ERR: Los ingredientes no se pudieron procesar"

    return chat_completion.choices[0].message.content

def confirm_token(token, expiration):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

def send_email(to, subject, template, attachment = None):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(sending(msg))

async def sending(msg):
    mail.send(msg)