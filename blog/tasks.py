from vertograd.celery import app
from blog.send_email_service import send
from order.save_order_service import order_create
from telebot import TeleBot
from celery import shared_task
from django.conf import settings

bot = TeleBot(settings.VER_G_MESSAGES_BOT)


@shared_task
def get_consultation_bot_message(application: dict):
    name = application.get('name')
    phone = application.get('phone')
    question = application.get('question')
    email = application.get('email')
    type_of_application = 'Бесплатная консультация'
    exactly_name_application = 'Бесплатная консультация'
    order_create(type_of_application=type_of_application,
                 exactly_name_application=exactly_name_application,
                 name=name, phone=phone, question=question, email=email)

    text = (f"На сайте ver-g оставлена заявка на бесплатную консультацию.\n\n"
            f"Имя: {name};\n"
            f"Телефон: {phone};"
            f"email: {email}\n\n"
            f"Текст вопроса: \n"
            f"{question}")
    bot.send_message(chat_id=settings.FORMS_AT_VER_G_CHAT_ID,
                     text=text)




