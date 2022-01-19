import time

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

GROUP_ID = "19366044"


def send(file, event_id):
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    vk.messages.send(
        peer_id=event_id,
        random_id=get_random_id(),
        message=text,
    )


vk_session = vk_api.VkApi(token="token")
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        id_event = event.message.from_id
        msg = event.message.text
        vk.messages.setActivity(
            user_id=id_event,
            group_id=GROUP_ID,
            type="typing"
        )
        time.sleep(1.5)
        if msg == "Начать":
            keyboard = VkKeyboard(one_time=False)

            keyboard.add_button('Время работы', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('Реквизиты', color=VkKeyboardColor.SECONDARY)
            keyboard.add_button('Как добраться', color=VkKeyboardColor.SECONDARY)

            keyboard.add_line()
            keyboard.add_button('Правила размещения постов', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('Групповые посещения', color=VkKeyboardColor.SECONDARY)
            keyboard.add_button('Нужды приюта', color=VkKeyboardColor.SECONDARY)

            vk.messages.send(
                user_id=id_event,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard(),
                message="Что бы вы хотели узнать?"
            )

        if msg == "Реквизиты":
            send("rekv.txt", id_event)
        elif msg == "Время работы":
            vk.messages.send(
                peer_id=id_event,
                random_id=get_random_id(),
                message="Мы открыты для посещения с 11 до 16-30! Групповые посещения (от 5 человек) нужно обговаривать отдельно с директором приюта. \n\n ☎ 904-903 Екатерина."
            )
        elif msg == "Правила размещения постов":
            send("rules.txt", id_event)
        elif msg == "Нужды приюта":
            send("needs.txt", id_event)
        elif msg == "Групповые посещения":
            send("groups.txt", id_event)
        elif msg == "Как добраться":
            send("root.txt", id_event)
            vk.messages.send(
                peer_id=id_event,
                random_id=get_random_id(),

                message="https://yandex.ru/maps/-/CCUIrVwegA",
                dont_parse_links=0
            )