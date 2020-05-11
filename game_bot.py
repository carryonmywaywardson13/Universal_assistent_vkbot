from random import random
from yandex_translate import YandexTranslate
import requests
import random
from datetime import datetime
import pytz
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
vk_session = vk_api.VkApi(
        token='3db404cca9293537d5090a80167c6cbe9823e858bd95a021372a1f60e6266f37dfa3b6f8660435691201e')
translate = YandexTranslate('trnsl.1.1.20200511T130644Z.6364d76cfdc43982.a4f1928c9916bafa41bcc6b8ee1e32fd790ba287')
longpoll = VkBotLongPoll(vk_session, 195107797)
vk = vk_session.get_api()

# trnsl.1.1.20200511T130644Z.6364d76cfdc43982.a4f1928c9916bafa41bcc6b8ee1e32fd790ba287
def main_tr():
    global vk_session
    global translate
    global longpoll
    global vk
    for event in longpoll.listen():
        flag = 0
        if event.type == VkBotEventType.MESSAGE_NEW:
                if event.type == VkBotEventType.MESSAGE_NEW:  # Если получили сообщение с текстом
                    trTo = event.object.message['text']
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.obj.message['from_id'],
                        message='Введите фразу, которую надо перевести ', random_id=random.randint(0, 2 ** 64)
                    )

                if event.type == VkBotEventType.MESSAGE_NEW:  # Если получили сообщение с текстом
                    trNormal = 1  # Колхозный флаг для ошибки
                    try:  # Исключение, о них поговорим ниже
                        trFrom = translate.detect(event.obj.message['text'])
                        trResult = translate.translate(event.obj.message['text'], trFrom + '-' + trTo)
                    except Exception as e:
                        trNormal = 0
                        print("Exception:", e)
                        pass
                    if trNormal == 1:
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            message='Переведено сервисом «Яндекс.Переводчик» translate.yandex.ru\n' + str(
                                trResult['text'], random_id=random.randint(0, 2 ** 64))
                        )
                        flag = 1
                        break

                    if trNormal == 0:
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            message='Неправильно введён язык', random_id=random.randint(0, 2 ** 64)
                        )
                        flag = 1
                        break

                if flag == 1:
                    break

def main_time():
    global vk_session
    global translate
    global longpoll
    global vk

    for event in longpoll.listen():
        if  event.type == VkBotEventType.MESSAGE_NEW:
            session['index_id'] = 1
            city_n_hour = event.object.message['text']
            tz = pytz.timezone(city_n_hour)
            city_current_datetime = datetime.now(tz)
            print(city_current_datetime)

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Time in {city_n_hour}: " + str(city_current_datetime),
                             random_id=random.randint(0, 2 ** 64))


def main_weather():
    global vk_session
    global translate
    global longpoll
    global vk



    for event in longpoll.listen():


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

            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
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

session = dict()
session['index_id'] = 0
running = True
while running:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if session['index_id'] != 1:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Hi! I am your personal assistant. To get started, write: "Start"',
                                 random_id=random.randint(0, 2 ** 64))

                if event.object.message['text'].lower() == 'start':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=('What would you like to see at the moment: \n'
                                              'WEATHER\n'
                                              'TIME\n'
                                              'TRANSLATOR'), random_id=random.randint(0, 2 ** 64))

                if event.object.message['text'].lower() == 'переводчик' or \
                        event.object.message['text'].upper() == 'TRANSLATOR':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='What is the language? Use two letters.\n '
                                             'For example: Russian - ru, English - en',
                                     random_id=random.randint(0, 2 ** 64))
                    main_tr()

                if event.object.message['text'].lower() == 'погода' or \
                        event.object.message['text'].upper() == 'WEATHER':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Great! How many days would you like '
                                             'to choose the weather forecast for? \n'
                                             'FOR A DAY\n'
                                             'FOR FIVE DAYS', random_id=random.randint(0, 2 ** 64))

                    main_weather()

                if event.object.message['text'].lower() == 'время' or \
                        event.object.message['text'].upper() == 'TIME':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='What is the language? Use two letters.\n '
                                             'For example: Russian - ru, English - en',
                                     random_id=random.randint(0, 2 ** 64))

                    main_time()





