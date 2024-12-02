from django.conf import settings
from celery import shared_task
from telebot import TeleBot
from order.save_order_service import order_create

bot = TeleBot(settings.VER_G_MESSAGES_BOT)

@shared_task
def get_service_bot_message(application: dict):
    name = application.get('name')
    phone = application.get('phone')
    email = application.get('email')
    question = application.get('question')
    service_name = application.get('service_name')
    order_create(type_of_application='Услуга',
                 exactly_name_application=service_name,
                 name=name, phone=phone, question=question, email=email)

    text = (f"На сайте ver-g оставлена заявка на услугу {service_name}\n\n"
            f"Имя: {name};\n"
            f"Телефон: {phone};\n"
            f"email: {email}\n\n"
            f"Текст вопроса: \n"
            f"{question}")
    bot.send_message(chat_id=settings.FORMS_AT_VER_G_CHAT_ID,
                     text=text)
