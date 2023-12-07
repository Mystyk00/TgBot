import requests
import telegram
from telegram.ext import Updater, CommandHandler
import random

city = 'Kyiv'

def weather(update, context):
    api_key = "3870ece1b4577e1fa7ff617d9923e4d7"
    city_name = city if city else "Київ"
    url =f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    weather_date = response.json()

    description = weather_date['weather'][0]['description']
    temperature = weather_date['main']['temp']

    message = f'Погода у місті {city_name}: {description}. Температура: {temperature} C'
    context.bot.send_message(chat_id = update.message.chat_id, text = message)

def help_command(update, context):
    availableCommands = [
        '/weather -> city: Show weather in city',
        '/set_city <from> -> <to>' ,
        '/predict: Prediction (always true btw)'
              ]
    help_text = f'Available commands \n ' +f'\n'.join(availableCommands)
    update.message.reply_text(help_text)

def set_city(update, context):
    global city
    newCity = f''.join(context.args)
    city = newCity
    update.message.reply_text(f'City succesfully changed to: {newCity}')

def predict(update, context):
    with open('predictions.txt', 'r', encoding='utf-8') as f:
        text = f.readlines()

    randomText = random.choice(text).strip()
    update.message.reply_text(f'Your prediction is: {randomText}')


def main():
    updater = Updater('6464946041:AAHwNMQ3nmf0moUHTy6JghdtoHPWkLmA5Ms')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('weather', weather))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('set_city', set_city))
    dispatcher.add_handler(CommandHandler('predict', predict))

    updater.start_polling()
    updater.idle()

main()