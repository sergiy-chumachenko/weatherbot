from weather_provider import OpenWeatherMapProvider

import logging
import os
import telebot

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how re you doing?")


@bot.message_handler(commands=['get_weather'])
def send_location(message):
    bot.reply_to(message, 'Push the button and send me your current location', reply_markup=get_weather())


@bot.message_handler(content_types=["location"])
def get_weather_from_location(message):
    if message.location:
        location = message.location.__dict__
        logging.info(message.__dict__)
        provider = OpenWeatherMapProvider(os.environ.get('OPEN_WEATHER_MAP_API_KEY'))
        current_weather = provider.get_current_weather(lon=location.get('longitude'), lat=location.get('latitude'))
        weather_info = provider.parse_weather_data(current_weather)
        send_weather_info(info=weather_info, chat_id=message.chat.id)


def send_weather_info(info, chat_id):
    bot.send_message(text=info, chat_id=chat_id)


def get_weather():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton(text='Send my location', request_location=True)
    markup.row(button)
    return markup


if __name__ == "__main__":
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)
    logging.info('WeatherBot initialization...')
    bot.polling()
