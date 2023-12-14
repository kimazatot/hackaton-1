
import telebot
from telebot import types
from main import main
from decouple import config

token = config('TOKEN')
bot = telebot.TeleBot(token)
data = []

inline_keyboard = types.ReplyKeyboardMarkup(row_width=5)
income_types = types.ReplyKeyboardMarkup(resize_keyboard=True)

for i in range(1, 21):
    inline_keyboard.add(types.KeyboardButton(str(i)))

income_types.add(types.KeyboardButton('Описание'), types.KeyboardButton('Фото'), types.KeyboardButton('Выход'))


@bot.message_handler(commands=['start'])
def start(message):
    global data
    bot.send_message(message.chat.id,
                     'Привет, извиняюсь за такой долгий ответ, надо мной еще работают, а пока мы парсим новости с KaktusMedia, подождите немного, пока будут все новости')

    data = main()
    bot.send_message(message.chat.id, 'Парсинг завершен')

    if not data:
        bot.send_message(message.chat.id, 'На сегодня нет новостей')

    news_text = ''
    for num, news in enumerate(data, start=1):
        news_text += f"{num}. {news[0]}\n"

    chunks = [news_text[i:i + 4000] for i in range(0, len(news_text), 4000)]  # Разделение текста на части по 4000 символов

    for chunk in chunks:
        bot.send_message(message.chat.id, 'Вот все новости:\n\n' + chunk, disable_notification=True)

    msg = bot.send_message(message.chat.id, 'Выберите номер новости, чтобы узнать подробнее:', reply_markup=inline_keyboard)
    bot.register_next_step_handler(msg, check)


def check(message):
    num = int(message.text) - 1
    if num >= len(data):
        bot.send_message(message.chat.id, 'Такой новости у нас нету')
        return

    msg = bot.send_message(message.chat.id, 'Можете посмотреть описание и фото', reply_markup=income_types)
    bot.register_next_step_handler(msg, get_info, num)


def get_info(message, num):
    if message.text.lower() == 'описание':
        bot.send_message(message.chat.id, data[num][2])
        bot.send_message(message.chat.id, data[num][1])
        msg = bot.send_message(message.chat.id, 'Что вы хотите сделать дальше?', reply_markup=income_types)
        bot.register_next_step_handler(msg, get_info, num)
    elif message.text.lower() == 'выход':
        bot.send_message(message.chat.id, 'До свидания!')
    elif message.text.lower() == 'фото':
        if data[num][1]:
            bot.send_photo(message.chat.id, data[num][1], caption="Фото к новости")
            msg = bot.send_message(message.chat.id, 'Что вы хотите сделать дальше?', reply_markup=income_types)
            bot.register_next_step_handler(msg, get_info, num)
        else:
            bot.send_message(message.chat.id, "К сожалению, фото к этой новости еще не загружено.")
            msg = bot.send_message(message.chat.id, 'Что вы хотите сделать дальше?', reply_markup=income_types)
            bot.register_next_step_handler(msg, get_info, num)
            
bot.polling()
