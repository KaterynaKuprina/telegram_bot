import telebot
from telebot import types
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

API_TOKEN = "6665239558:AAGklogkngMithUSjSOrWbTYc9K_wYuwX0w"
GOOGLE_CREDENTIALS_FILE = "/Users/madalica/PycharmProjects/pythonProject/pythonProject/telegram_bot_3.0/refined-cortex-383811-222f72067798.json"
bot = telebot.TeleBot(API_TOKEN)


def check_date_availability(date):
    credentials = Credentials.from_authorized_user_file(GOOGLE_CREDENTIALS_FILE)
    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', timeMin=date + 'T00:00:00Z',
                                          timeMax=date + 'T23:59:59Z').execute()
    events = events_result.get('items', [])
    return not events


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message, "Добро пожаловать! Чем я могу помочь?"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_info = types.KeyboardButton("Инфо")
    btn_booking = types.KeyboardButton("Бронь")
    btn_events = types.KeyboardButton("Мероприятия")
    btn_other_services = types.KeyboardButton("Другие услуги")
    btn_shop = types.KeyboardButton("Магазин")
    btn_manager = types.KeyboardButton("Менеджер")

    markup.add(btn_info, btn_booking)
    markup.add(btn_events, btn_other_services)
    markup.add(btn_shop, btn_manager)

    bot.send_message(
        message.from_user.id,
        f"Привет, {message.from_user.first_name}! Я ваш помощник",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Инфо")
def send_info(message):
    bot.send_message(
        message.chat.id,
        "Информация о студии: адрес, контакты, описание услуг, режим работы."
    )


@bot.message_handler(func=lambda message: message.text == "Бронь")
def make_booking(message):
    msg = bot.send_message(message.chat.id, "Введите дату для бронирования в формате YYYY-MM-DD:")
    bot.register_next_step_handler(msg, process_date_step)


def process_date_step(message):
    try:
        date_to_check = message.text.strip()
        date_obj = datetime.datetime.strptime(date_to_check, "%Y-%m-%d").date()
        today = datetime.date.today()
        if date_obj >= today:
            availability = check_date_availability(date_to_check)
            if availability:
                bot.send_message(message.chat.id, f"Дата {date_to_check} доступна для бронирования.")
            else:
                bot.send_message(message.chat.id, f"Дата {date_to_check} занята.")
        else:
            bot.send_message(message.chat.id, "Неверная дата. Введите будущую дату.")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат даты. Нажмите кнопку Бронь и попробуйте еще раз.")


@bot.message_handler(func=lambda message: message.text == "Выбрать дату")
def choose_date(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton("Да")
    btn_no = types.KeyboardButton("Нет")
    markup.add(btn_yes, btn_no)

    bot.send_message(
        message.chat.id,
        "Вы готовы забронировать на выбранную дату?",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "Да")
def confirm_booking(message):
    # Здесь можно добавить логику отправки сообщения администратору
    bot.send_message(
        message.chat.id,
        "Ваш запрос на бронирование отправлен администратору. Мы свяжемся с вами для подтверждения."
    )


@bot.message_handler(func=lambda message: message.text == "Нет")
def cancel_booking(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_choose_date = types.KeyboardButton("Выбрать дату")
    btn_contact_manager = types.KeyboardButton("Связаться с менеджером")
    markup.add(btn_choose_date, btn_contact_manager)

    bot.send_message(
        message.chat.id,
        "Выберите другую дату или свяжитесь с менеджером для помощи.",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "Мероприятия")
def send_events(message):
    bot.send_message(
        message.chat.id,
        "Информация о предстоящих мероприятиях или ссылка на канал Telegram студии."
    )


@bot.message_handler(func=lambda message: message.text == "Другие услуги")
def other_services(message):
    bot.send_message(
        message.chat.id,
        "Информация о мастер-классах, фотосессиях, девичниках/мальчишниках и других услугах студии."
    )


@bot.message_handler(func=lambda message: message.text == "Магазин")
def send_shop(message):
    bot.send_message(
        message.chat.id,
        "Посетите интернет-магазин студии, где вы можете приобрести товары, связанные с деятельностью студии."
    )


@bot.message_handler(func=lambda message: message.text == "Менеджер")
def contact_manager(message):
    bot.send_message(
        message.chat.id,
        "Вы перешли в чат с менеджером студии. Задайте свои вопросы или получите помощь в оформлении заказа."
    )


bot.polling()
