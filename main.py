import requests
import telebot
from telebot import types
from geopy.geocoders import Nominatim

url = "https://hotels4.p.rapidapi.com/locations/search"

bot = telebot.TeleBot("1875127679:AAFuKvDtEgDMPDzdr8gyiD2lGFZ6R1srYhc", parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Для продолжения работы бота требуется доступ к геопозиции", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude
        geolocator = Nominatim(user_agent='hotel')
        loc = geolocator.reverse(f'{latitude}, {longitude}', exactly_one=True)
        address = loc.raw['address']
        city = address.get('city', '')
        if city == '':
            city = address.get('town', '')
        print(city)
        navigaton(message, city)


def navigaton(message, city: str):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_low = types.KeyboardButton(text="Топ самых дешевых отелей")
    button_high = types.KeyboardButton(text="Топ самых дорогих отелей")
    button_user = types.KeyboardButton(text="Гибкий поиск")
    keyboard.add(button_low, button_high, button_user)
    bot.send_message(message.chat.id, "Выберите метод поиска",
                     reply_markup=keyboard)





bot.polling()