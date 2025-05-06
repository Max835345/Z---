import telebot
from telebot import types
import smtplib
from email.mime.text import MIMEText

# Настройки бота
TOKEN = '7716148906:AAFLbjfneJnUAp8ALAgrTJkgziw4IDbtq7Y'
bot = telebot.TeleBot(TOKEN)

# Настройки почты Mail.ru
MAILRU_EMAIL = 'gert.maks@inbox.ru'
MAILRU_PASSWORD = 'NZgL51b0hiwwJRq5TiS3'
RECIPIENT_EMAIL = 'gert.maks@inbox.ru'

# Список профессий
PROFESSIONS = [
    "👷 Строитель в инженерные войска",
    "🚁 Оператор БПЛА",
    "🔧 Механик в ремонтный батальон",
    "📡 Связист",
    "🚛 Водитель снабжения",
    "💥 Артиллерист (заряжающий, наводчик, механик)",
    "🛡️ Специалист ПВО",
    "⚔️ Боец штурмового отряда"
]

# Временное хранилище данных
user_data = {}


class UserData:
    def __init__(self):
        self.full_name = None
        self.age = None
        self.phone = None
        self.region = None
        self.diseases = None
        self.profession = None


# --- Клавиатуры ---
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📝 Начать заполнение анкеты"))
    return markup


def get_cancel_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    return markup


def get_profession_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(p) for p in PROFESSIONS]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("❌ Отмена"))
    return markup


# --- Команды бота ---
@bot.message_handler(commands=['start', 'restart'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = UserData()

    bot.send_message(
        chat_id,
        "👋 Добро пожаловать! Я бот для сбора анкетных данных.\n\n"
        "Нажмите кнопку ниже, чтобы начать:",
        reply_markup=get_main_keyboard()
    )


# --- Обработка анкеты ---
@bot.message_handler(func=lambda message: message.text == "📝 Начать заполнение анкеты")
def start_filling(message):
    chat_id = message.chat.id
    user_data[chat_id] = UserData()

    msg = bot.send_message(
        chat_id,
        "📝 Введите ваше ФИО:",
        reply_markup=get_cancel_keyboard()
    )
    bot.register_next_step_handler(msg, process_full_name)


@bot.message_handler(func=lambda message: message.text == "❌ Отмена")
def cancel_filling(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "❌ Заполнение анкеты отменено.",
        reply_markup=get_main_keyboard()
    )


def process_full_name(message):
    chat_id = message.chat.id
    if message.text == "❌ Отмена":
        return cancel_filling(message)

    user_data[chat_id].full_name = message.text
    msg = bot.send_message(
        chat_id,
        "🔢 Сколько вам лет?",
        reply_markup=get_cancel_keyboard()
    )
    bot.register_next_step_handler(msg, process_age)


def process_age(message):
    chat_id = message.chat.id
    if message.text == "❌ Отмена":
        return cancel_filling(message)

    try:
        age = int(message.text)
        if age <= 0 or age > 120:
            raise ValueError
        user_data[chat_id].age = age

        msg = bot.send_message(
            chat_id,
            "👔 Выберите вашу профессию:",
            reply_markup=get_profession_keyboard()
        )
        bot.register_next_step_handler(msg, process_profession)
    except ValueError:
        msg = bot.send_message(
            chat_id,
            "❌ Некорректный возраст! Введите число от 1 до 120.",
            reply_markup=get_cancel_keyboard()
        )
        bot.register_next_step_handler(msg, process_age)


def process_profession(message):
    chat_id = message.chat.id
    if message.text == "❌ Отмена":
        return cancel_filling(message)

    if message.text not in PROFESSIONS:
        msg = bot.send_message(
            chat_id,
            "❌ Пожалуйста, выберите профессию из списка:",
            reply_markup=get_profession_keyboard()
        )
        bot.register_next_step_handler(msg, process_profession)
        return

    user_data[chat_id].profession = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📱 Отправить номер", request_contact=True))
    markup.add(types.KeyboardButton("❌ Отмена"))

    msg = bot.send_message(
        chat_id,
        "📱 Отправьте ваш номер телефона:",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, process_phone)


def process_phone(message):
    chat_id = message.chat.id
    if message.text == "❌ Отмена":
        return cancel_filling(message)

    if message.contact:
        user_data[chat_id].phone = message.contact.phone_number
    else:
        user_data[chat_id].phone = message.text

    msg = bot.send_message(
        chat_id,
        "🌍 Введите ваш регион проживания:",
        reply_markup=get_cancel_keyboard()
    )
    bot.register_next_step_handler(msg, process_region)


def process_region(message):
    chat_id = message.chat.id
    if message.text == "❌ Отмена":
        return cancel_filling(message)

    user_data[chat_id].region = message.text

    msg = bot.send_message(
        chat_id,
        "🏥 Есть ли у вас хронические болезни? Опишите, если да:",
        reply_markup=get_cancel_keyboard()
    )
    bot.register_next_step_handler(msg, process_diseases)


def process_diseases(message):
    chat_id = message.chat.id
    if message.text == "❌ Отмена":
        return cancel_filling(message)

    user_data[chat_id].diseases = message.text

    # Формируем письмо
    data = user_data[chat_id]
    email_text = f"""
    🚀 Новые данные клиента:
    --------------------------
    👤 ФИО: {data.full_name}
    🔢 Возраст: {data.age}
    👔 Профессия: {data.profession}
    📱 Телефон: {data.phone}
    🌍 Регион: {data.region}
    🏥 Болезни: {data.diseases}
    --------------------------
    """

    # Отправка на почту
    if send_email(email_text):
        bot.send_message(
            chat_id,
            "✅ Данные успешно отправлены! Спасибо!\n\n"
            "Если хотите заполнить анкету заново, нажмите /start",
            reply_markup=get_main_keyboard()
        )
    else:
        bot.send_message(
            chat_id,
            "❌ Ошибка отправки. Попробуйте позже.",
            reply_markup=get_main_keyboard()
        )


# --- Отправка email через Mail.ru ---
def send_email(text):
    try:
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['Subject'] = 'Анкета клиента из Telegram-бота'
        msg['From'] = MAILRU_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(MAILRU_EMAIL, MAILRU_PASSWORD)
        server.sendmail(MAILRU_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)








