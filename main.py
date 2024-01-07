import telebot
from telebot import types

API_TOKEN = "6665239558:AAGklogkngMithUSjSOrWbTYc9K_wYuwX0w"

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message, "Вас приветствует телеграм-бот РОАН студии. Чем я могу быть полезен?"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Бронь")
    btn2 = types.InlineKeyboardButton("Менеджер", url="https://google.com")
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton("Информация")
    btn4 = types.InlineKeyboardButton("Телеграм-канал", url="https://google.com")
    markup.row(btn3, btn4)
    bot.send_message(
        message.from_user.id,
        f"Привет {message.from_user.first_name}! Я твой бот-помощник",
        reply_markup=markup,
    )


@bot.message_handler(content_types=["text"])
def menu(message):
    if message.text == "Бронь":
        bot.send_message(
            message.chat.id,
            "Напишите, пожалуйста, на какую дату Вы хотите забронировать и я поищу для Вас свободное время в этот день",
        )
        bot.register_next_step_handler(message, reserve)  # TODO
    elif message.text == "Информация":
        bot.send_message(
            message.chat.id,
            "Тут общая информация. если хотите дополнительную информацию, то нажмите кнопочку информация еще раз. Если хотите попасть в главное меню, то нажмите Назад",
        )
        if message.text == "Информация":
            bot.register_next_step_handler(message, info)
        else:
            bot.register_next_step_handler(message, send_welcome)
    elif message.text == "Мероприятия":
        bot.send_message(
            message.chat.id,
            "Вот список запланированых мероприятий на ближайшее время: ",
        )
    elif message.text == "Другие услуги":
        bot.send_message(message.chat.id, "Позже вставлю нужный текст")
    elif message.text == "Магазин":
        bot.send_message(message.chat.id, "Позже вставлю нужный текст")
    elif message.text == "Главное меню":
        bot.register_next_step_handler(message, send_welcome)



@bot.message_handler(commands=["info"])
def info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Мероприятия")
    btn2 = types.KeyboardButton("Магазин")
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton("Другие услуги")
    btn4 = types.KeyboardButton("Главное меню")
    markup.row(btn3, btn4)
    bot.send_message(
        message.from_user.id,
        """Если Вас иснтересуют мероприятия, запланированые на ближайшее время, то нажмите кнопку Мероприятия. 
                     Если вас интересует ассортимент магазина, то нажмите кнопку Магазин. Для информации о других событиях студии, надмите Другие услуги """,
        reply_markup=markup,
    )


def reserve():
    pass


def store():
    pass


def event():
    pass


def services():
    pass


def chanel():
    pass


bot.infinity_polling()
