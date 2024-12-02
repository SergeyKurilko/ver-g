import re

from celery import shared_task
from telebot import TeleBot
from django.utils.formats import date_format
from django.conf import settings


messages_bot = TeleBot(settings.VER_G_MESSAGES_BOT)

# Бот для работы с админкой (присылает промо-коды, создаваемые в админке)
bot_for_admin = TeleBot(settings.VER_G_MESSAGES_BOT)


@shared_task
def send_telegram_promo(promo: dict):
    """
    Отправляет сообщение в telegram при создании нового промокода в
    админке.
    """
    if promo['validity_period']:
        # Форматируем дату в нужный формат
        validity_period_str = 'до ' + date_format(promo['validity_period'], 'd E Y')
    else:
        validity_period_str = 'Бессрочный'

    text = (f'Скидка: {promo["sale_value"]}%\n'
            f'Курс: [{promo["course_title"]}](https://ver-g.ru{promo["course_absolute_url"]})\n\n'
            f'Код: `{promo["code"]}`\n'
            f'Срок действия: {validity_period_str}')
    bot_for_admin.send_message(chat_id=settings.ADMIN_VER_G_CHAT_ID, text=text, parse_mode='markdown')


@shared_task
def send_telegram_step_comment(comment: dict):
    """
    Отправляет сообщение с комментарием, оставленным к шагу.
    В comment: dict ожидается 4 ключа
    "comment_pk" - pk нового объекта CommentForStep
    "current_step_pk" - pk объекта StepForPoint, к которому оставлен комментарий
    "author_email" - email автора
    "date" - дата
    "text" - текст комментария
    """
    date_str = date_format(comment["date"], 'd E Yг.')

    text = (f'<b style="color: green">В шаге id{comment["current_step_pk"]} оставлен комментарий;</b>\n'
            f'Комментарий id{comment["comment_pk"]} от {date_str};\n'
            f'Автор {comment["author_email"]};\n\n'
            f'Текст комментария: \n'
            f'{comment["text"]}')

    # Из формы приходит сообщение с тегами <p></p> Telegram их не принимает
    # При помощи регулярного выражения, уберем их
    clean_text = re.sub(r'<p>|</p>', ' ', text)
    messages_bot.send_message(chat_id=settings.COMMENTS_FROM_VER_G_CHAT_ID, text=clean_text, parse_mode='HTML')


@shared_task
def send_telegram_register_new_user(new_user: dict):
    first_name = new_user.get("first_name", "не указано")
    last_name = new_user.get("last_name", "не указано")
    email = new_user.get("email", "не указано")

    text = (f"На площадке ver-g/academy зарегистрирован новый пользователь.\n"
            f"Имя: {first_name};\n"
            f"Фамилия: {last_name};\n"
            f"email: {email}"
            )
    bot_for_admin.send_message(chat_id=settings.EDUCATION_PLATFORM_ACTIVITY_CHAT_ID, text=text)


@shared_task
def send_telegram_create_access_to_course(course_access: dict):
    user_email = course_access.get("user_email")
    training_course = course_access.get("training_course")
    text = (f"Оформлена подписка на курс.\n"
            f"Пользователь: {user_email}\n"
            f"Курс: {training_course}")
    bot_for_admin.send_message(chat_id=settings.EDUCATION_PLATFORM_ACTIVITY_CHAT_ID, text=text)



