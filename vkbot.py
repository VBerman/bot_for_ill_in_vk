# -*- coding: utf-8 -*-
import vk_api
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import time, os
#при запуске интернет должен быть в любом случае
id_admin = []
session = vk_api.VkApi(
    token='')
longpoll = vk_api.bot_longpoll.VkBotLongPoll(session, )
vk = session.get_api()
student_list = [{"Фамилия": "Пример", "id": 1, "Статус": None}]
json_keyboard_first_message = {
            "one_time": True,
            "buttons": [
                [{
                "action": {
                    "type": "text",
                    "payload": {"buttons": "1"},
                    "label": "Все в порядке",
                    },
                "color": "positive"
                },
                {
                "action": {
                    "type": "text",
                    "payload": {"buttons": "2"},
                    "label": "Болею",
                    },
                "color": "negative"
                }],
                [{
                "action": {
                    "type": "text",
                    "payload": {"buttons": "3"},
                    "label": "Я отпишу, если что-то случится",
                    },
                "color": "primary"
                }]
                 ]
            }

json_keyboard_ill = {
            "one_time": True,
            "buttons": [[{
                "action": {
                    "type": "text",
                    "payload": {"buttons": "1"},
                    "label": "Обращался ко врачу",
                    },
                "color": "primary"
                },
                         {
                "action": {
                    "type": "text",
                    "payload": {"buttons": "2"},
                    "label": "На справке",
                    },
                "color": "primary"
                }

                 ]]
            }
def send_mess():
    message_text = "Как ты себя сегодня чувствуешь?"
    for item in student_list:
        try:
            if item['Статус'] == None:
                vk.messages.send(user_id=item['id'], random_id=get_random_id(), message=(message_text), keyboard=json.dumps(json_keyboard_first_message))
        except:
            item['Статус'] = "Пользователь не разрешил присылать себе сообщения."
        time.sleep(0.5)
def send_bye(id_acc):
    message = 'Я записал твой ответ.'
    vk.messages.send(user_id=id_acc, random_id=get_random_id(),
                     message=message)
def main():
    print("Бот включен")
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print('Новое сообщение:')
                id = int(event.message.from_id)
                input_message_text = event.message.text
                print('Для меня от: ', end='')

                print(id)

                print('Текст:', input_message_text)
                for item in student_list:
                    if (item['id'] == id) and (item['Статус'] == None):
                        if input_message_text == "Все в порядке":
                            item['Статус'] = 'Все в порядке'
                            send_bye(id)
                        elif input_message_text == 'Болею':
                            item['Статус'] = 'Болеет'
                            message = 'Соболезную, ходил ли ты к врачу или сидишь на справке?'
                            vk.messages.send(user_id=item['id'], random_id=get_random_id(),
                                             message=(message),
                                             keyboard=json.dumps(json_keyboard_ill))
                        elif input_message_text == 'Я отпишу, если что-то случится':
                            item['Статус'] = 'Отказался от рассылки'
                            send_bye(id)
                        else:
                            vk.messages.send(user_id=item['id'], random_id=get_random_id(), message=("Я не понимаю таких команд :c"),
                                             keyboard=json.dumps(json_keyboard_first_message))
                    elif (item['id'] == id) and (item['Статус'] == "Болеет"):
                        if input_message_text == 'Обращался ко врачу':
                            item['Статус'] = "Обращался ко врачу"
                            send_bye(id)
                        elif input_message_text == 'На справке':
                            item['Статус'] = "На справке"
                            send_bye(id)
                        else:
                            vk.messages.send(user_id=item['id'], random_id=get_random_id(),
                                             message=("Я не понимаю таких команд :c"),
                                             keyboard=json.dumps(json_keyboard_ill))
                message =''
                if input_message_text == "Предоставь мне выкладку":
                    sick = 0
                    healthy = 0
                    not_answered_yet = 0
                    forbidden_to_send_messages = 0
                    unsubscribe = 0
                    for item in id_admin:
                        if item == id:
                            for items in student_list:
                                message += str(items['Фамилия']) + ' - ' + str(items['Статус'])+'\n'
                                if items['Статус'] == "На справке" or items['Статус'] == "Обращался ко врачу":
                                    sick += 1
                                elif items['Статус'] == "Все в порядке":
                                    healthy +=1
                                elif items['Статус'] == None:
                                    not_answered_yet +=1
                                elif items['Статус'] == "Пользователь не разрешил присылать себе сообщения.":
                                    forbidden_to_send_messages += 1
                                elif items['Статус'] == 'Отказался от рассылки':
                                    unsubscribe += 1
                            message += "Больных: " + str(sick) + ". В процентах: " + str(sick/len(student_list)*100) + "%.\n"
                            message += "Здоровых: " + str(healthy) + ". В процентах: " + str(healthy/len(student_list)*100) + "%.\n"
                            message += "Не ответивших: " + str(not_answered_yet) + ". В процентах: " + str(not_answered_yet/len(student_list)*100) + "%.\n"
                            message += "Не разрешивших прислать сообщение: " + str(forbidden_to_send_messages) + ". В процентах: " + str(forbidden_to_send_messages/len(student_list)*100) + "%.\n"
                            message += "Отписавшихся от рассылки: " + str(unsubscribe) + ". В процентах: " + str(unsubscribe/len(student_list)*100) + "%.\n"
                            vk.messages.send(user_id=item, random_id=get_random_id(),
                                             message=(message))
                if input_message_text == "End" and id == id_admin[0]:
                    os.abort()
                    print('Бот выключен')



    except:
        print("Отсутствует соединение с сервером.")
        print("Бот выключен")
        time.sleep(30)


if __name__ == '__main__':
    exit_command = False
    send_mess()
    while  exit_command != True:
        main()
