from random import random

from googletrans import Translator
import googletrans

import requests
import random
from datetime import datetime
import pytz
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def main_tr():
    vk_session = vk_api.VkApi(
        token='3db404cca9293537d5090a80167c6cbe9823e858bd95a021372a1f60e6266f37dfa3b6f8660435691201e')
    translator = Translator()
    longpoll = VkBotLongPoll(vk_session, 195107797)
    vk = vk_session.get_api()

    session = dict()
    session['index_id'] = 0
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            '''if session['index_id'] != 1:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                message='Hi! I am your personal assistant. To get started, write: "Start"',
                                random_id=random.randint(0, 2 ** 64))
                session['index_id'] = 1
            if event.object.message['text'].lower() == 'start':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('What would you like to see at the moment: \n'
                                          'WEATHER\n'
                                          'TIME\n'
                                          'TRANSLATOR'), random_id=random.randint(0, 2 ** 64))'''



            if event.object.message['text'].lower() == 'переводчик' or \
                    event.object.message['text'].upper() == 'TRANSLATOR':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                message='What is the language? Use two letters.\n '
                                        'For example: Russian - ru, English - en',
                                random_id=random.randint(0, 2 ** 64))
            exit1 = 0

            if event.object.message['text'].lower() in googletrans.LANGUAGES:
                save_tr = event.object.message['text']
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Enter the phrase to translate ',
                                 random_id=random.randint(0, 2 ** 64))

            if not(event.object.message['text'].lower()) in googletrans.LANGUAGES\
                    and len(event.object.message['text'].lower()) != 0:
                Error_tr = 1
                try:
                    # переводим на данный язык
                    result = translator.translate(save_tr, dest=event.obj.message['from_id'])

                except Exception as e:
                    # если не заработало
                    Error_tr = 0
                    print("Exception:", e)
                    pass

                if Error_tr == 1:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='translated by Google Translator\n' + str(result),
                                     random_id=random.randint(0, 2 ** 64))


def main_time():
    vk_session = vk_api.VkApi(
        token='3db404cca9293537d5090a80167c6cbe9823e858bd95a021372a1f60e6266f37dfa3b6f8660435691201e')
    translator = Translator()
    longpoll = VkBotLongPoll(vk_session, 195107797)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text:
            city_n_hour = event.type
            if city_n_hour == 'Moscow':
                current_datetime = datetime.now()
                print(current_datetime)

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Time in Moscow: " + str(current_datetime),
                                 random_id=random.randint(0, 2 ** 64))
            else:
                tz = pytz.timezone(city_n_hour)
                city_current_datetime = datetime.now(tz)
                print(city_current_datetime)

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Time in {city_n_hour}: " + str(current_datetime),
                                 random_id=random.randint(0, 2 ** 64))



def main_weather():
    vk_session = vk_api.VkApi(
        token='3db404cca9293537d5090a80167c6cbe9823e858bd95a021372a1f60e6266f37dfa3b6f8660435691201e')
    translator = Translator()
    longpoll = VkBotLongPoll(vk_session, 195107797)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            city = event.obj.message['text']
            city_id = 0
            app_id = "буквенно-цифровой APPID"
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/find",
                                   params={'q': city,
                                           'type': 'like', 'units': 'metric', 'APPID': app_id})
                data = res.json()
                cities = ["{} ({})".format(d['name'], d['sys']['country'])
                          for d in data['list']]
                print("city:", cities)
                city_id = data['list'][0]['id']
                print('city_id=', city_id)
            except Exception as e:
                print("Exception (find):", e)
                pass

            vk.messages.send(chat_id=event.obj.message['from_id'],
                             message='Great! How many days would you like '
                                     'to choose the weather forecast for? \n'
                                     'FOR A DAY\n'
                                     'FOR FIVE DAYS', random_id=random.randint(0, 2 ** 64))

            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.type == 'FOR A DAY':
                        try:
                            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                               params={'id': city_id, 'units': 'metric', 'lang': 'ru',
                                                       'APPID': app_id})
                            data = res.json()

                            if event.from_chat:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"conditions: "
                                                         f"{data['weather'][0]['description']}",
                                                 random_id=random.randint(0, 2 ** 64))

                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"temperature: "
                                                         f"{data['main']['temp']}",
                                                 random_id=random.randint(0, 2 ** 64))

                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f" minimum temperature: "
                                                         f"{data['main']['temp _min']}",
                                                 random_id=random.randint(0, 2 ** 64))

                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f" maximum temperature: "
                                                         f"{data['main']['temp _max']}",
                                                 random_id=random.randint(0, 2 ** 64))


                        except Exception as e:
                            print("Exception (weather):", e)
                            pass


                        if event.type == 'FOR FIVE DAYS':
                            try:
                                res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                                                   params={'id': city_id, 'units': 'metric',
                                                           'lang': 'ru',
                                                           'APPID': app_id})
                                data = res.json()
                                for i in data['list']:
                                    print(i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']),
                                          i['weather'][0]['description'])

                                    if event.from_chat:
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message=f"{i['dt_txt']} "
                                                                 f"{'{0:+3.0f}'.format(i['main']['temp'])} "
                                                                 f"{i['weather'][0]['description']}",
                                                         random_id=random.randint(0, 2 ** 64))


                            except Exception as e:
                                print("Exception (forecast):", e)
                                pass


vk_session = vk_api.VkApi(
        token='3db404cca9293537d5090a80167c6cbe9823e858bd95a021372a1f60e6266f37dfa3b6f8660435691201e')
    translator = Translator()
    longpoll = VkBotLongPoll(vk_session, 195107797)
    vk = vk_session.get_api()

running = True

while running:



if __name__ == '__main__':
    main_tr()
