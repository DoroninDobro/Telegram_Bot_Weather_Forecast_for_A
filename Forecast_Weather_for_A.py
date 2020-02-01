import pyowm
import telebot
from config import TOKEN, OWM_TOKEN
from random import randint
from telebot import types

bot = telebot.TeleBot(TOKEN)
owm = pyowm.OWM(OWM_TOKEN, language = "ru")

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('hello.jpeg', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Привет!\nЯ -твой личный предсказатель! \nЫЫЫ! =))")

@bot.message_handler(content_types=['text'])
def send_echo(message):
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

    if 'пасмурно' in answer or 'дождь' in answer or 'ливень' in answer:
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

bot.polling(none_stop=True)
