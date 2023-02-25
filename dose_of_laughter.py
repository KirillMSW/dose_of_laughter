import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import re


token_file=open('token.txt')
TOKEN = token_file.read()
if '\n' in TOKEN:
    TOKEN = TOKEN[:-1]
token_file.close()

VK = vk_api.VkApi(token=TOKEN)

LONGPOLL = VkLongPoll(VK)

composite_req_dict = {}

main_keyboard={
                "one_time": False,
                "buttons": [
                [{
                    "action": {
                    "type": "text",
                    "label": "Получить дозу смеха"
                    },
                    "color": "primary"
                }]
            ]}


def write_msg(user_id, message,keyboard):
    '''
    Sends text message to user
    :param user_id:
    :param message:
    :return:
    '''
    VK.method('messages.send', {'user_id': user_id, 'random_id': get_random_id(),
                                'message': message, 'keyboard':json.dumps(keyboard,ensure_ascii=False)})


for event in LONGPOLL.listen():

    try:
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                msg = VK.method('messages.getById', {'message_ids': event.message_id})
                request = event.text

                if request=='Получить дозу смеха':
                    write_msg(event.user_id,"ЖОПА", main_keyboard)
                else:
                    write_msg(event.user_id,
                              'Для получения дозы смеха нажмите на кнопку \"Получить дозу смеха\"', main_keyboard)
    except Exception:
        pass
