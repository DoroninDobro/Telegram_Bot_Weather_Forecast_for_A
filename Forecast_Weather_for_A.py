import pyowm  # package for forecast of weather
import telebot
from config import TOKEN, OWM_TOKEN
from random import randint
from telebot import types  # import buttons
import datetime

bot = telebot.TeleBot(TOKEN)
owm = pyowm.OWM(OWM_TOKEN, language="ru")


@bot.message_handler(commands=['start'])  # it is welcome part
def welcome(message):
    sti = open('hello.jpeg', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Привет!\nЯ -твой личный предсказатель! \nЫЫЫ! =))")


@bot.message_handler(content_types=['text'])
def send_echo(message):
    # another city
    if message.chat.type == 'private':
        user_text = message.text
        if message.text[0:5] == 'City ' or message.text[0:5] == 'city ':
            try:
                nc = user_text[5:]    # new_city
                Nc = owm.weather_at_place(nc)
                w_Nc = Nc.get_weather()
                temp_Nc = w_Nc.get_temperature('celsius')["temp"]
                answer3 = "В " + nc + ' ' + w_Nc.get_detailed_status()+'\n'
                answer3 += "Температура в среднем " + str(temp_Nc) + '\n\n'
                bot.send_message(message.chat.id, answer3)
            except Exception as e:
                answer4 = 'Я не знаю такого города, наверное там хорошо :-)'
                bot.send_message(message.chat.id, answer4)
        # My first easter egg for culture people))
        elif user_text[1:5] == 'hank' or user_text[1:7] == 'пасибо':
            if 22 > datetime.datetime.now().hour > 6:
                sti4 = open('niceday.jpeg', 'rb')
                bot.send_sticker(message.chat.id, sti4)
            else:
                sti5 = open('good_night.jpeg', 'rb')
                bot.send_sticker(message.chat.id, sti5)
        # mainpart: Forecast for Saint-Petersburg
        else:
            SP = owm.weather_at_place('Санкт-Петербург')
            Bali = owm.weather_at_place('Jakarta')

            w_SP = SP.get_weather()
            w_Bali = Bali.get_weather()

            temp_SP = w_SP.get_temperature('celsius')["temp"]
            temp_Bali = w_Bali.get_temperature('celsius')["temp"]

            answer = "В Питере сейчас " + w_SP.get_detailed_status()+'\n'
            answer += "Температура в среднем " + str(temp_SP) + '\n\n'

            if temp_SP < 10:
                answer += 'Уууу, зная твою мерзлявость тебе стоит приодеться. =( \n'
            elif temp_SP < 20:
                answer += 'Ну не жарко, захвати с собой что-то для утепления, особенно вечером. 4-1 <3 \n'
            else:
                answer += 'Ммм, неплохо, одевайся как хочешь, самое время показать всем свою красоту! =)) \n'
            answer += 'Зато на Бали сейчас ' + str(temp_Bali) + '! И манго!'

            # add stickers =))
            if 'дождь' in answer or 'ливень' in answer:
                x_r = randint(1, 7)
                name = f'rain{x_r}.jpeg'
                stik = open(name, 'rb')
                bot.send_sticker(message.chat.id, stik)
            if 'солнечно' in answer or 'солнце' in answer:
                sti2 = open('sun.jpeg', 'rb')
                bot.send_sticker(message.chat.id, sti2)
                bot.send_message(message.chat.id, 'Ну наконец-то! Бросай все и беги за витамином D!')
                answer = "Температура сейчас " + str(temp_SP) + '\n\n'
            bot.send_message(message.chat.id, answer)

            # buttons and instructions about other cities
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Да!", callback_data='good')

            markup.add(item1)
            bot.send_message(message.chat.id, 'Хочешь узнать погоду в другом городе?', reply_markup=markup)


# function proccesing answer
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                help_message = ("Напиши слово 'City', пробел и затем название "
                                'по английски, убедись что оно '
                                'совпадает с названием латиницей на гугл-картах, '
                                'совсем маленькие города могут не '
                                'отображаться, я еще маленький =)')
                bot.send_message(call.message.chat.id, help_message)

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)  # bor work non-stop
