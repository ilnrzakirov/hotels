import requests
import json
import telebot
from .models import Profile, Message
from django.conf import settings
from hotelapp.management.commands.bot import logger

url = "https://hotels4.p.rapidapi.com/locations/search"

@logger.catch()
def get_city_id(call: telebot.types.CallbackQuery):
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


    for item in data['suggestions']:
        if item['group'] == 'CITY_GROUP':
            for i_item in item['entities']:
                city = Profile.objects.get(extr_id=call.message.chat.id).city
                if i_item['type'] == "CITY" and i_item['name'] == city:
                    Profile.objects.filter(extr_id=call.message.chat.id).update(city_id=int(i_item['destinationId']))
                elif i_item['type'] == "CITY" and city in i_item['name']:
                    Profile.objects.filter(extr_id=call.message.chat.id).update(city_id=int(i_item['destinationId']))

@logger.catch()
def get_list_hotel(call):
    pass
