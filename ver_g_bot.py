import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
import locale
from dotenv import load_dotenv
from datetime import datetime, timedelta
import aiohttp
import redis
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

redis_connect = redis.Redis(db=1)

API_TOKEN = os.getenv("VER_G_MESSAGES_BOT")
API_URL_PREFIX = os.getenv("API_URL_PREFIX")
API_URL_FOR_GET_COURSES_QUERY = os.getenv("API_URL_FOR_GET_COURSES_QUERY")
API_URL_FOR_CREATE_PROMO_FOR_COURSE = os.getenv("API_URL_FOR_CREATE_PROMO_FOR_COURSE")
API_URL_FOR_CHECK_PROMO_FOR_COURSE = os.getenv("API_URL_FOR_CHECK_PROMO_FOR_COURSE")
API_URL_FOR_GET_REPORT_EDUCATION_PLATFORM = os.getenv("API_URL_FOR_GET_REPORT_EDUCATION_PLATFORM")
ADMIN_VER_G_CHAT_LINK = os.getenv("ADMIN_VER_G_CHAT_LINK")
API_URL_FOR_DELETE_COMMENT_FOR_ARTICLE = os.getenv("API_URL_FOR_DELETE_COMMENT_FOR_ARTICLE")
# Чат с комментариями оставленными в блоге и в шагах
COMMENTS_FROM_VER_G_CHAT_ID = os.getenv("COMMENTS_FROM_VER_G_CHAT_ID")
# Чат для работы с админкой и БД
ADMIN_VER_G_CHAT_ID = os.getenv("ADMIN_VER_G_CHAT_ID")
# Оповещения об активностях на ver-g/academy
EDUCATION_PLATFORM_ACTIVITY_CHAT_ID = os.getenv("EDUCATION_PLATFORM_ACTIVITY_CHAT_ID")
# ID админов, допущенных к использованию бота
ELENA_CHAT_ID = os.getenv("ELENA_CHAT_ID")
SERGEY_CHAT_ID = os.getenv("SERGEY_CHAT_ID")
# API KEY для использования api
API_KEY_VER_G = os.getenv("API_KEY_VER_G")

bot = AsyncTeleBot(API_TOKEN)

def format_data(date_str: str):
    """
    Преобразует строку в объект datetime.
    Объект datetime преобразует в строку нужного формата '00 месяц 2025'
    """
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    # Преобразуем строку в объект datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Преобразуем объект datetime в строку нужного формата
    date_string = datetime.strftime(date_obj, "%d %B %Y")

    return date_string

def create_start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Добавляем кнопку "Статистика сайта" в первый ряд
    markup.row(KeyboardButton("Статистика сайта📈"))
    # Добавляем кнопки "Создать промокод к курсу" и "Проверить промокод" во второй ряд
    markup.row(KeyboardButton("Создать промокод к курсу 🍪"), KeyboardButton("Проверить промокод 🔍"))
    return markup


def register_handlers(bot):
    # Обработка команды \start
    @bot.message_handler(commands=["start"])
    async def start_keyboard_sender(message):
        if str(message.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            markup = create_start_keyboard()
            await bot.send_message(message.chat.id, "Что будем делать сегодня?", reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, "Это частный бот. Обратитесь к владельцу.")

    # Обработка команды \test
    @bot.message_handler(commands=["test"])
    async def test_command(message):
        if str(message.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(message.chat.id, "Я тут.")
        else:
            await bot.send_message(message.chat.id, "Это частный бот. Обратитесь к владельцу.")

    # обработка сообщения Дай айди
    @bot.message_handler(func=lambda message: message.text == "Дай айди")
    async def get_id_handler(message):
        if str(message.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            user_id = message.from_user.id
            await bot.send_message(message.chat.id, f"Твой ID: `{user_id}`",
                                   parse_mode='markdown')
        else:
            await bot.send_message(message.chat.id, "Это частный бот. Обратитесь к владельцу.")

    # обработка нажатия кнопки "Создать промокод к курсу 🍪"
    @bot.message_handler(func=lambda message: message.text == "Создать промокод к курсу 🍪")
    async def get_courses_query_for_create_promo_code(message):
        if not str(message.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(message.chat.id, "Это частный бот. Обратитесь к владельцу.")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'{API_URL_PREFIX}{API_URL_FOR_GET_COURSES_QUERY}',
                    params={"API_KEY_VER_G": API_KEY_VER_G}
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()

                        markup = InlineKeyboardMarkup()
                        for course in response_data:
                            markup.add(InlineKeyboardButton(
                                text=f"{course['id']} {course['title']}",
                                callback_data=f"create_promo_for_{course['id']}_{course['slug']}"))

                        await bot.send_message(message.chat.id,
                                               "Список курсов получен. Пожалуйста, "
                                               "выберите курс для создания промокода.",
                                               reply_markup=markup)
                    else:
                        await bot.send_message(message.chat.id, "Произошла ошибка при получении списка курсов.")

    # Обработка после нажатия на кнопку с курсом
    @bot.callback_query_handler(func=lambda call: call.data.startswith('create_promo_for_'))
    async def create_promo_for_course(call):
        if not str(call.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(call.chat.id, "Это частный бот. Обратитесь к владельцу.")
        else:
            course_pk = call.data.split("_")[-2]
            course_slug = call.data.split("_")[-1]
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("5%",
                                            callback_data=f"continue_create_promo_for_{course_pk}"
                                                          f"_sale_5"))
            markup.add(InlineKeyboardButton("25%",
                                            callback_data=f"continue_create_promo_for_{course_pk}"
                                                          f"_sale_25"))
            markup.add(InlineKeyboardButton("50%",
                                            callback_data=f"continue_create_promo_for_{course_pk}"
                                                          f"_sale_50"))
            markup.add(InlineKeyboardButton("100%",
                                            callback_data=f"continue_create_promo_for_{course_pk}"
                                                          f"_sale_100"))
            await bot.send_message(chat_id=call.message.chat.id,
                                   text=f"Выбери размер скидки для курса {course_slug}",
                                   reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)


    # Обработка после нажатия на кнопку с размером скидки
    @bot.callback_query_handler(func=lambda call: call.data.startswith('continue_create_promo_for_'))
    async def continue_create_promo(call):
        if not str(call.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(call.chat.id, "Это частный бот. Обратитесь к владельцу.")
        else:
            sale_value = call.data.split("_")[-1]
            course_pk = call.data.split("_")[-3]
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text="1 Месяц",
                                            callback_data=f"ending_create_promo_for_{course_pk}"
                                                          f"_sale_{sale_value}_period_1"))
            markup.add(InlineKeyboardButton(text="2 Месяца",
                                            callback_data=f"ending_create_promo_for_{course_pk}"
                                                          f"_sale_{sale_value}_period_2"))
            markup.add(InlineKeyboardButton(text="Бессрочно",
                                            callback_data=f"ending_create_promo_for_{course_pk}"
                                                          f"_sale_{sale_value}_period_infinitely"))
            await bot.send_message(chat_id=call.message.chat.id,
                                   text=f"Выбери срок действия промокода",
                                   reply_markup=markup)
            await bot.delete_message(call.message.chat.id, call.message.message_id)

    # Выбор срока действия промокода и завершение создания промокода
    @bot.callback_query_handler(func=lambda call: call.data.startswith('ending_create_promo_for_'))
    async def ending_create_promo_code(call):
        if not str(call.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(call.chat.id, "Это частный бот. Обратитесь к владельцу.")
        else:
            sale_value = call.data.split("_")[-3]
            course_pk = call.data.split("_")[-5]
            period = call.data.split("_")[-1]

            if period != "infinitely":
                validity_period = ((datetime.now() + timedelta(days=int(period) * 30))).strftime('%Y-%m-%d')
            else:
                validity_period = None

            # Отправка запроса на api
            async with aiohttp.ClientSession(trust_env=True) as session:
                json_data = {
                    "course_pk": course_pk,
                    "sale_value": sale_value,
                    "validity_period": validity_period,
                    "API_KEY_VER_G": API_KEY_VER_G
                }
                async with session.post(url=f"{API_URL_PREFIX}{API_URL_FOR_CREATE_PROMO_FOR_COURSE}",
                                        json=json_data, headers={'Content-Type': 'application/json'},
                                        allow_redirects=False) as response:
                    if response.status == 201:
                        response_data = await response.json()

                        new_promo_code = {
                            "sale": response_data['sale_value'],
                            "course_title": response_data["course_title"],
                            "course_absolute_url": response_data["course_absolute_url"],
                            "code": response_data["code"]
                        }

                        period = response_data['validity_period']

                        if period:
                            # Форматируем дату в нужный формат
                            validity_period_str = f'до {format_data(period)}г.'
                        else:
                            validity_period_str = 'Бессрочный'

                        new_promo_code["period"] = validity_period

                        text = (f'Скидка: {new_promo_code["sale"]}%\n'
                                f'Курс: [{new_promo_code["course_title"]}]'
                                f'(https://ver-g.ru{new_promo_code["course_absolute_url"]})\n\n'
                                f'Код: `{new_promo_code["code"]}`\n'
                                f'Срок действия: {validity_period_str}')

                        await bot.send_message(chat_id=call.message.chat.id,
                                               text=text, parse_mode='markdown')

                        await bot.delete_message(call.message.chat.id, call.message.message_id)

    # Отслеживание нажатия кнопки "Проверить промокод 🔍"
    @bot.message_handler(func=lambda message: message.text == "Проверить промокод 🔍")
    async def check_promo_message(message):
        if not str(message.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(message.chat.id, "Это частный бот. Обратитесь к владельцу.")
        else:
            await bot.send_message(message.chat.id, "Для проверки промокода просто отправь его мне, но перед"
                                                 " промокодом допиши '*Промо*'. Должно быть примерно вот так: \n"
                                                 "'ПромоQFvUv1NQ' где 'QFvUv1NQ' - это промокод.",
                                   parse_mode='markdown')

    # Отслеживание получения промокода. Ожидается строка, начинающаяся с 'Промо'
    @bot.message_handler(func=lambda message: message.text.startswith('Промо'))
    async def check_promo_code(message):
        if not str(message.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(message.chat.id, "Это частный бот. Обратитесь к владельцу.")
        else:
            if len(message.text) != 13:
                await bot.send_message(message.chat.id, "🚫\n"
                                                        "Неверный формат промокода. Промокод должен "
                                                        "состоять из 8 символов. Перед промокодом "
                                                        "допиши '*Промо*'",
                                       parse_mode='markdown')
            else:
                promo_code = message.text[5:13]

                async with aiohttp.ClientSession() as session:
                    json_data = {
                        "API_KEY_VER_G": API_KEY_VER_G,
                        "code": promo_code
                    }
                    url = f"{API_URL_PREFIX}{API_URL_FOR_CHECK_PROMO_FOR_COURSE}"
                    async with session.post(url, json=json_data, headers={'Content-Type': 'application/json'},
                                        allow_redirects=False) as response:
                        if response.status == 404:
                            await bot.send_message(message.chat.id,
                                                   "Промокод не найден.🙅‍♂️")
                        elif response.status == 200:
                            response_data = await response.json()

                            new_promo_code = {
                                "sale": response_data['sale_value'],
                                "course_title": response_data["course_title"],
                                "course_absolute_url": response_data["course_absolute_url"],
                                "code": response_data["code"]
                            }

                            period = response_data['validity_period']

                            if period:
                                # Форматируем дату в нужный формат
                                validity_period_str = f'до {format_data(period)}г.'
                            else:
                                validity_period_str = 'Бессрочный'

                            new_promo_code["period"] = validity_period_str

                            text = (f'✅\n'
                                    f'Скидка: {new_promo_code["sale"]}%\n'
                                    f'Курс: [{new_promo_code["course_title"]}]'
                                    f'(https://ver-g.ru{new_promo_code["course_absolute_url"]})\n\n'
                                    f'Код: `{new_promo_code["code"]}`\n'
                                    f'Срок действия: {validity_period_str}')

                            await bot.send_message(chat_id=message.chat.id,
                                                   text=text, parse_mode='markdown')

    # обработка нажатия кнопки "Статистика сайта📈"
    @bot.message_handler(func=lambda message: message.text == "Статистика сайта📈")
    async def get_education_platform_report(message):
        if not str(message.from_user.id) in [ELENA_CHAT_ID, SERGEY_CHAT_ID]:
            await bot.send_message(message.chat.id, "Это частный бот. Обратитесь к владельцу.")
        else:
            async with aiohttp.ClientSession() as session:
                url = f"{API_URL_PREFIX}{API_URL_FOR_GET_REPORT_EDUCATION_PLATFORM}"
                try:
                    async with session.get(url=url, params={"API_KEY_VER_G": API_KEY_VER_G}) as response:
                        if response.status == 200:
                            response_data = await response.json()

                            text = (f"*Статистика сайта.*🔍📊\n\n"
                                    f"*Пользователи*🙍‍♀️🙎‍♂️🙆‍♂️🙆‍♀️\n"
                                    f"Всего: {response_data['total_users_number']}🙋🏻‍♂️\n"
                                    f"Новые пользователи: {response_data['last_12_hours_registrations']}🆕\n\n"
                                    f"*Курсы*📖📚📘\n"
                                    f"Всего курсов: {response_data['total_courses_number']}📚\n"
                                    f"Опубликованных: {response_data['total_published_courses_number']}🫣\n"
                                    f"Платные: {response_data['total_paid_courses_number']}🫰🫰\n"
                                    f"Бесплатные: {response_data['total_free_courses_number']}🎁")
                            await bot.send_message(chat_id=message.chat.id,
                                                   text=text,
                                                   parse_mode='markdown')


                            await bot.delete_message(message.chat.id, message.message_id)
                        else:
                            error_message = f"Ошибка при получении данных: {response.status}"
                            await bot.send_message(message.chat.id, error_message)
                except aiohttp.ClientError as e:
                    error_message = f"Ошибка при выполнении запроса: {e}"
                    await bot.send_message(message.chat.id, error_message)
                except Exception as e:
                    error_message = f"Непредвиденная ошибка: {e}"
                    await bot.send_message(message.chat.id, error_message)



    # Удаление комментария для статьи. Сообщение в чат приходит из comments.tasks.py
    # Обработчик нажатия на кнопку "Удалить"
    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete_comment_'))
    async def confirm_delete_comment_callback(call):
        # Извлекаем pk комментария из callback_data
        comment_id = call.data.split('_')[-1]


        # Создаем инлайн-клавиатуру с подтверждением
        markup = InlineKeyboardMarkup()
        yes_button = InlineKeyboardButton(text="Да", callback_data=f"delete_comment_{comment_id}")
        no_button = InlineKeyboardButton(text="Нет", callback_data="cancel_delete")
        markup.add(yes_button, no_button)

        # Отправляем сообщение с подтверждением
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Точно удалить комментарий?",
            reply_markup=markup
        )

    # Обработчик нажатия на кнопку "Да"
    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_comment_'))
    async def delete_comment_callback(call):

        # Извлекаем pk комментария из callback_data
        comment_id = call.data.split('_')[-1]

        # id отправителя
        tele_id = str(call.from_user.id)

        # Отправляем запрос на удаление комментария через API
        async with aiohttp.ClientSession() as session:
            url = f'{API_URL_PREFIX}{API_URL_FOR_DELETE_COMMENT_FOR_ARTICLE}'
            json_data = {
                "API_KEY_VER_G": API_KEY_VER_G,
                "comment_id": comment_id
            }
            async with session.delete(
                    url=url, params=json_data, allow_redirects=False
            ) as response:


                if response.status == 200:
                    response_data = await response.json()
                    if 'success' in response_data:
                        # Извлечение ключа из redis (он туда записывается в момент отправки
                        # сообщения в comments.tasks.send_telegram_message)
                        message_id_in_bytes = redis_connect.get(f"comment_message_id_{comment_id}")
                        message_id = int(message_id_in_bytes)
                        if message_id:
                            # удаление сообщения с комментарием из чата
                            await bot.delete_message(call.message.chat.id, message_id)
                            # удаление сообщения с подтверждением удаления из чата
                            await bot.delete_message(call.message.chat.id, call.message.message_id)
                            await redis_connect.delete(f"comment_message_id_{comment_id}")
                            await bot.answer_callback_query(call.id, text="Комментарий удален")
                            await bot.send_message(call.message.chat.id, response_data['success'])
                        else:
                            await bot.send_message(call.message.chat.id, "Нет данных в кэше. Вероятно, комментарий оставлен"
                                                                   " более двух дней назад.")
                            await bot.delete_message(call.message.chat.id, call.message.message_id)

                    elif 'error' in response_data:
                        await bot.answer_callback_query(call.id, text="Ошибка при удалении комментария")
                        await bot.send_message(call.message.chat.id, response_data['error'])
                        await bot.delete_message(call.message.chat.id, call.message.message_id)
                else:
                    await bot.answer_callback_query(call.id, text="Ошибка при удалении комментария")
                    await bot.send_message(call.message.chat.id, "Произошла ошибка при удалении комментария")

    # Обработчик нажатия на кнопку "Нет"
    @bot.callback_query_handler(func=lambda call: call.data == "cancel_delete")
    async def cancel_delete_callback(call):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(call.id, text="Удаление отменено")


# Регистрируем обработчики
register_handlers(bot)

async def main():
    await bot.infinity_polling()

# Запускаем бота
if __name__ == "__main__":
    asyncio.run(main())