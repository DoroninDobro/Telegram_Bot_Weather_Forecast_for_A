import pyowm
import telebot

bot = telebot.TeleBot("880795081:AAGrql1vXt1644l8CBoLtDdnU_R1kUzo8Wg")
owm = pyowm.OWM('8d4d7111350ee99f5b0607450670f05c', language = "ru")

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

    bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True)
