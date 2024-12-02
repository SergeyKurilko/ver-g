import redis
from celery import shared_task
from django.conf import settings
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = TeleBot(settings.VER_G_MESSAGES_BOT)

redis_connect = redis.Redis(db=1)


@shared_task
def send_telegram_message(chat_id, message, comment_id):
    # Создаем инлайн-клавиатуру
    markup = InlineKeyboardMarkup()
    delete_button = InlineKeyboardButton(
        text="Удалить",
        callback_data=f"confirm_delete_comment_{comment_id}"
    )
    markup.add(delete_button)

    # Отправляем сообщение с инлайн-клавиатурой
    sent_message = bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='markdown',
        reply_markup=markup
    )

    # Сохраняем message_id для последующего удаления в Redis
    redis_connect.set(f"comment_message_id_{comment_id}", sent_message.message_id, ex=172800)






    