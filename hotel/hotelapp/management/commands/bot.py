import telebot
from django.conf import settings
from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from telebot import types

from hotelapp.models import Profile, Message


def registration(message):
    p, flag = Profile.objects.get_or_create(
        extr_id=message.chat.id,
        defaults={
            'name' : message.chat.username
        }
    )
    Message(
        profile=p,
        text=message.text
    ).save()


class Command(BaseCommand):
    help: 'Телеграм чат бот'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TOKEN, parse_mode="HTML")
        print(bot.get_me())

        @bot.message_handler(commands=['start'])
        def start_bot(message):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
            keyboard.add(button_geo)
            registration(message)
            bot.send_message(message.chat.id, "Для продолжения работы бота требуется доступ к геопозиции",
                             reply_markup=keyboard)

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
                message.text = city
                registration(message)
                navigaton(message, city)
            else:
                bot.send_message(message.chat.id, "Не удается загрузить геоданные")

        def navigaton(message, city: str):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_low = types.KeyboardButton(text="Топ самых дешевых отелей")
            button_high = types.KeyboardButton(text="Топ самых дорогих отелей")
            button_user = types.KeyboardButton(text="Гибкий поиск")
            keyboard.add(button_low, button_high, button_user)
            bot.send_message(message.chat.id, "Выберите метод поиска",
                             reply_markup=keyboard)

        # @bot.message_handler(commands=['Топ самых дешевых отелей'])
        # def
        #    print('тут')

        bot.polling()