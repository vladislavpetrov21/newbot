import telebot
import random

bot = telebot.TeleBot()
keyboard = telebot.types.ReplyKeyboardMarkup()
key = telebot.types.ReplyKeyboardMarkup()
keys = telebot.types.ReplyKeyboardMarkup()
keyboard.row('для начинающих', 'посмотреть информацию')
key.row('мужской', 'женский')
keyboard.row('мотивашка')
keys.row('силовая', 'воркаут', 'бег')
sex = ''


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Бот Спортик поможет тебе получить полезную информацию про занятия спортом!'
                                      'он найдет тебе статьи и видео для начинающих занятия спортом!'
                                      'также бот умеет заряжать тебя мотивацией, с помощью цитат!')
    bot.send_message(message.chat.id, 'Используй эти команды для общения с ботом:\n'
                                      '/start - начать общение\n'
                                      '/help - получить информацию про бота\n')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, {}! Вижу что ты захотел(а) заняться спортом) Молодец!'
                     .format(message.from_user.first_name), reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Используй эти команды для общения с ботом:\n'
                                      '/start - начать общение\n'
                                      '/help - получить информацию про бота\n')
    bot.send_message(message.chat.id, 'Если тебе нужна информация для начинающих, то жми "для начинающих"!\n'
                                      'Если ты не новичок, то жми "посмотреть информацию"!\n'
                                      'Если нужна мотивация, то "мотивашка" тебе поможет!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'для начинающих':
        bot.send_message(message.chat.id, 'Какой тренировкой займемся?)', reply_markup=keys)
        bot.register_next_step_handler(message, start_training)
    elif message.text.lower() == 'посмотреть информацию':
        bot.send_message(message.chat.id, 'Отлично! Введи пол', reply_markup=key)
        bot.register_next_step_handler(message, get_sex)
    elif message.text.lower() == 'мотивашка':
        bot.send_message(message.chat.id, 'Цитата на сегодня: ')
        send_quotes(message)
        send_sticker(message)
    else:
        bot.send_message(message.chat.id, 'Извини, {}, но я тебя не понимаю('.format(message.from_user.first_name))


def get_info(message):
    if sex == 'мужской':
        bot.send_message(message.chat.id, 'Прекрасно! Мы вместе добьемся результата!!!', reply_markup=keyboard)
        try:
            with open('men_info', encoding='UTF-8') as info:
                information = info.read()
        except IOError:
            print('An IOError has occurred!')
        finally:
            info.close()
        bot.send_message(message.from_user.id, text=information)
    elif sex == 'женский':
        bot.send_message(message.chat.id, 'Прекрасно! Мы вместе добьемся результата!!!', reply_markup=keyboard)
        try:
            with open('women_info', encoding='UTF-8') as info:
                information = info.read()
        except IOError:
            print('An IOError has occurred!')
        finally:
            info.close()
        bot.send_message(message.from_user.id, text=information)
    else:
        bot.send_message(message.chat.id, 'Извини, {}, но я тебя не понимаю('.format(message.from_user.first_name))
        start_message(message)


def get_sex(message):
    global sex
    sex = message.text
    get_info(message)


def send_quotes(message):
    quot_list = []
    try:
        with open("quotes", encoding='UTF-8') as quot:
            today_quot = quot.read()
            for string in today_quot.split('\n'):
                quot_list.append(string)
    except IOError:
        print('An IOError has occurred!')
    finally:
        quot.close()
    rand_quot = random.choice(quot_list)
    bot.send_message(message.chat.id, rand_quot)


def start_training(message):
    if message.text.lower() == 'силовая':
        bot.send_message(message.chat.id, 'Отлично!')
        start_gym(message)
    elif message.text.lower() == 'воркаут':
        bot.send_message(message.chat.id, 'Круто!')
        start_workout(message)
    elif message.text.lower() == 'бег':
        bot.send_message(message.chat.id, 'Начнем!')
        start_run(message)
    else:
        bot.send_message(message.chat.id, 'Извини, {}, но я тебя не понимаю('.format(message.from_user.first_name))


def start_run(message):
    bot.send_message(message.chat.id, 'Полезные статьи про бег:', reply_markup=keyboard)
    adr = "https://marathonec.ru/kak-nachat-begat/"
    bot.send_message(message.chat.id, adr)


def start_gym(message):
    bot.send_message(message.chat.id, 'Полезные статьи про занятия в зале:', reply_markup=keyboard)
    adr = "https://fitnavigator.ru/trenirovki/programmy/trenirovok-dlja-nachinajushhih.html"
    bot.send_message(message.chat.id, adr)


def start_workout(message):
    bot.send_message(message.chat.id, 'Полезные статьи про воркаут:', reply_markup=keyboard)
    adr = "https://fitnavigator.ru/trenirovki/programmy/na-turnike-dlja-nachinajushhih-programma.html"
    bot.send_message(message.chat.id, adr)


def send_sticker(message):
    sticker_list = []
    try:
        with open("stickers") as sticker:
            today_sticker = sticker.read()
            for string in today_sticker.split('\n'):
                sticker_list.append(string)
    except IOError:
        print('An IOError has occurred!')
    finally:
        sticker.close()
    rand_sticker = random.choice(sticker_list)
    bot.send_sticker(message.chat.id, rand_sticker)


bot.polling()
