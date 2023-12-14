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

    for num, news in enumerate(data, start=1):
        bot.send_message(message.chat.id, f"{num}. {news[0]}")

    msg = bot.send_message(message.chat.id, 'Какую новость показать подробнее?', reply_markup=inline_keyboard)
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

