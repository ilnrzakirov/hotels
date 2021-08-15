import telebot
from django.conf import settings
from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from telebot import types
from loguru import logger

from hotelapp.models import Profile, Message
from hotelapp.lowprice import get_lowprice

logger.add("logging.log", format="{time}, {level}, {message}", level="DEBUG")


@logger.catch()
def registration(message, city=None):
    p, flag = Profile.objects.get_or_create(
        extr_id=message.chat.id,
        # city = city,
        defaults={
            'city': city,
            'name': message.chat.username,
        }
    )
    Message(
        profile=p,
        text=message.text
    ).save()


@logger.catch()
class Command(BaseCommand):
    help: 'Телеграм чат бот'

    @logger.catch()
    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TOKEN, parse_mode="HTML")

        @bot.message_handler(commands=['start'])
        @logger.catch()
        def start_bot(message):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
            keyboard.add(button_geo)
            bot.send_message(message.chat.id, "Для продолжения работы бота требуется доступ к геопозиции",
                             reply_markup=keyboard)

        @bot.message_handler(content_types=["location"])
        @logger.catch()
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
                print(loc)
                message.text = city
                registration(message, city)
                Profile.objects.filter(extr_id=message.chat.id).update(city=city)
                keyboard = types.InlineKeyboardMarkup(row_width=1, )
                button_location = types.InlineKeyboardButton(
                    text=f"Поиск в городе {Profile.objects.get(extr_id=message.chat.id).city}", callback_data='/city')
                button_city = types.InlineKeyboardButton(text="Поиск в другом городе", callback_data='/user_city')
                keyboard.row(button_location)
                keyboard.row(button_city)
                bot.send_message(message.chat.id, "Выберите город", reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, "Не удается загрузить геоданные")

        @bot.callback_query_handler(func=lambda call: call.data == '/city')
        @logger.catch()
        def city_for_geo(call):
            navigaton(call.message)

        @bot.callback_query_handler(func=lambda call: call.data == '/user_city')
        @logger.catch()
        def user_city(call):
            bot.send_message(call.message.chat.id, "Введите название города, "
                                                   "допускается добавлять в поиск название страны, региона итд."
                                                   " Например (Россия Москва) ")

            @bot.message_handler(content_types=['text'])
            def get_city(message):
                city = message.text
                geolocator = Nominatim(user_agent='hotel')
                if geolocator.geocode(city):
                    loc = geolocator.geocode(city, exactly_one=True, language='ru')
                    loc = geolocator.reverse(f'{loc.latitude}, {loc.longitude}', exactly_one=True, language='ru')
                    address = loc.raw['address']
                    city = address.get('city', '')
                    if city == '':
                        city = address.get('town', '')
                        if city == '':
                            city = address.get('village', '')
                    bot.send_message(call.message.chat.id,
                                     f'Город для поиска - {city}, {address.get("country")} что бы изменить город '
                                     f'просто наберите название города еще раз')
                    Profile.objects.filter(extr_id=call.message.chat.id).update(city=city)
                    navigaton(message)
                else:
                    bot.send_message(call.message.chat.id, "Такого города не существует, попробуйте еще раз")

        @logger.catch()
        def navigaton(message):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            button_low = types.InlineKeyboardButton(text="Топ самых дешевых отелей", callback_data='/lowprice')
            button_high = types.InlineKeyboardButton(text="Топ самых дорогих отелей", callback_data='/highprice')
            button_user = types.InlineKeyboardButton(text="Гибкий поиск", callback_data='/bestdeal')
            keyboard.row(button_low)
            keyboard.row(button_high)
            keyboard.row(button_user)
            bot.send_message(message.chat.id, "Выберите метод поиска",
                             reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: call.data == '/lowprice')
        @logger.catch()
        def lowprice(call):
            get_lowprice(call)

        @bot.callback_query_handler(func=lambda call: call.data == '/highprice')
        @logger.catch()
        def highprice(call):
            pass

        @bot.callback_query_handler(func=lambda call: call.data == '/highprice')
        @logger.catch()
        def bestdeal(call):
            pass

        bot.polling()
