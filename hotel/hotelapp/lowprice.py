import json

import telebot
import requests

from .models import Profile, Message
from django.conf import settings
from hotelapp.management.commands.bot import logger

url = "https://hotels4.p.rapidapi.com/locations/search"

@logger.catch()
def get_lowprice(call: telebot.types.CallbackQuery):
    querystring = {"query":f"{Profile.objects.get(extr_id=call.message.chat.id).city}", "locale":"ru_RU"}
    print(Profile.objects.get(extr_id=call.message.chat.id).city)
    headers = {
        'x-rapidapi-key': settings.API_KEY,
        'x-rapidapi-host': "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)

    with open('data.txt', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)





