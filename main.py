import requests
import telebot
from telebot import types
from geopy.geocoders import Nominatim

url = "https://hotels4.p.rapidapi.com/locations/search"

bot = telebot.TeleBot("1875127679:AAFuKvDtEgDMPDzdr8gyiD2lGFZ6R1srYhc", parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.reply_to(message, "Для продолжения работы бота требуется доступ к геопозиции")
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Отправить местоположение", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude
        geolocator = Nominatim(user_agent='hotel')
        city = geolocator.reverse(f'{latitude}, {longitude}')
        print(city)

bot.polling()