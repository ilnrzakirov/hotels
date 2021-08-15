import telebot

from .models import Profile, Message
from hotelapp.management.commands.bot import logger
from .hotel_api import get_city_id

url = "https://hotels4.p.rapidapi.com/locations/search"


@logger.catch()
def get_highprice(call: telebot.types.CallbackQuery):
    get_city_id(call)
