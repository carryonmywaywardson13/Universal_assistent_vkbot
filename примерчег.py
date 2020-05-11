'''   if event.text == 'Переводчик' or event.text.upper() == 'TRANSLATOR':
                    if event.from_chat:
                        # фразы
                        vk.messages.send(chat_id=event.chat_id,
                                         message='What is the language? Use two letters.\n '
                                                 'For example: Russian - ru, English - en',
                                         random_id=random.randint(0, 2 ** 64))
                    exit1 = 0
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text:
                            save_tr = event.text

                            if event.from_chat:
                                # если вести беседу
                                vk.messages.send(chat_id=event.chat_id,
                                                 message='Enter the phrase to translate ',
                                                 random_id=random.randint(0, 2 ** 64))

                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text:
                            # Если получили сообщение с текстом
                            Error_tr = 1

                            try:
                                # переводим на данный язык
                                result = translator.translate(save_tr, dest=event.text)

                            except Exception as e:
                                # если не заработало
                                Error_tr = 0
                                print("Exception:", e)
                                pass

                            if Error_tr == 1:  # Если всё хорошо


                                if event.from_chat:
                                    # Для диалога
                                    vk.messages.send(user_id=event.chat_id,
                                                     message='translated by Google Translator\n' + str(result),
                                                     random_id=random.randint(0, 2 ** 64))
                                    exit1 = 1  # выход из цикла
                                    break

                            if Error_tr == 0:

                                if event.from_chat:
                                    # Отправляем сообщение
                                    vk.messages.send(user_id=event.chat_id,
                                                     message='Sorry, but I do not know that language! Try again.',
                                                     random_id=random.randint(0, 2 ** 64))

                                    exit1 = 1  # выход из цикла
                                    break

                        if exit1 == 1:
                            break

                if event.text.upper == 'ПОГОДА' or event.text.upper() == 'WEATHER':
                    vk.messages.send(user_id=event.user_id,
                                     message="What city's weather do you want to know?",
                                     random_id=random.randint(0, 2 ** 64))

                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text:
                            city = event.type
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

                            vk.messages.send(chat_id=event.chat_id,
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
                                                vk.messages.send(user_id=event.chat_id_id,
                                                                 message=f"conditions: "
                                                                         f"{data['weather'][0]['description']}",
                                                                 random_id=random.randint(0, 2 ** 64))

                                                vk.messages.send(user_id=event.chat_id,
                                                                 message=f"temperature: "
                                                                         f"{data['main']['temp']}",
                                                                 random_id=random.randint(0, 2 ** 64))

                                                vk.messages.send(user_id=event.chat_id,
                                                                 message=f" minimum temperature: "
                                                                         f"{data['main']['temp _min']}",
                                                                 random_id=random.randint(0, 2 ** 64))

                                                vk.messages.send(user_id=event.chat_id,
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
                                                        vk.messages.send(user_id=event.chat_id,
                                                                         message=f"{i['dt_txt']} "
                                                                                 f"{'{0:+3.0f}'.format(i['main']['temp'])} "
                                                                                 f"{i['weather'][0]['description']}",
                                                                         random_id=random.randint(0, 2 ** 64))


                                            except Exception as e:
                                                print("Exception (forecast):", e)
                                                pass

                if event.text.upper == 'ВРЕМЯ' or event.text.upper() == 'TIME':
                    vk.messages.send(user_id=event.chat_id_id,
                                     message="Time in which city would you like to get?",
                                     random_id=random.randint(0, 2 ** 64))

                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.to_me and event.text:
                            city_n_hour = event.type
                            if city_n_hour == 'Moscow':
                                current_datetime = datetime.now()
                                print(current_datetime)

                                vk.messages.send(user_id=event.chat_id,
                                                 message="Time in Moscow: " + str(current_datetime),
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                tz = pytz.timezone(city_n_hour)
                                city_current_datetime = datetime.now(tz)
                                print(city_current_datetime)

                                vk.messages.send(user_id=event.chat_id_id,
                                                 message=f"Time in {city_n_hour}: " + str(current_datetime),
                                                 random_id=random.randint(0, 2 ** 64))'''

if event.obj.message['text'] == 'Start':
    print(event.obj.message['text'])
    vk = vk_session.get_api()
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=('What would you like to see at the moment: \n'
                              'WEATHER\n'
                              'TIME\n'
                              'TRANSLATOR'), random_id=random.randint(0, 2 ** 64))
