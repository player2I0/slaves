import re

from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Next, Back, SwitchTo, NumberedPager, ScrollingGroup
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format, List

from aiogram.types import User, ContentType, Message
from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link, decode_payload

from magic_filter import F

from db import User as UserDB

import states

async def home_getter(dialog_manager: DialogManager, event_from_user: User, db_user: UserDB, bot: Bot, **kwargs):
    #print('get!')
    data = {'has_slaves': False, 'has_owner': False}

    locale = {
        "welcome": {"en": "Hello"},
        "link": {'en': "Your link: ", "ru": "Ваша ссылка: "},
        "back": {"en": "‹ Back", "ru": "‹ Назад"},
        "get_link": {"en": "Your link", "ru": "Ваша ссылка"},
        "slaves": {"en": "Your slaves", "ru": "Ваши рабы"},
        "slaves_tip": {"en": "Send a message with slave's index to get info about the slave.", "ru": "Отправьте сообщение с номером раба, чтобы узнать о нём больше."}
    }

    if db_user.is_enslaved():
        owner = db_user.get_owner()
        locale['status'] = {'en': "You are currently a slave of " + owner.name, "ru": "Вы находитесь в рабстве. Ваш хозяин - " + owner.name}
    else:
        locale['status'] = {'en': "You are currently free", "ru": "Вы (пока что) свободны"}

        if len(db_user.slaves) > 0:
            data['has_slaves'] = True

    data = data | states.user_locale(locale, event_from_user.language_code) #merge two dicts together (python 3.9+)

    data['link'] = await create_start_link(bot, str(event_from_user.id), encode=True)

    return data

async def slaves_getter(dialog_manager: DialogManager, event_from_user: User, db_user: UserDB, **kwargs):
    l = []
    i = 0

    for slave_id in db_user.slaves:
        slave = UserDB.get(UserDB.id == slave_id)

        l.append((slave.name, i))
        
        i += 1

    return {'slaves': l}

async def slave_number_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager, **kwargs):
    slave_index = re.sub(r"\D+", '', message.text)
    #print(slave_index)
    await message.delete()

    if len(slave_index) > 0:
        slave_index = int(slave_index)
        
        db_user = UserDB.get(UserDB.id == message.from_user.id)

        if slave_index <= len(db_user.slaves):
            await dialog_manager.start(state=states.SlaveManager.info, data={'popup': True})
    
    dialog_manager.show_mode = ShowMode.EDIT

dialog = Dialog(
    Window(
        Format("{l_status}"),  # just a constant text
        #Button(Const("Useless button"), id="nothing"),  # button with text and id
        Next(Format("{l_get_link}")),
        SwitchTo(Format("{l_slaves}"), state=states.Home.slaves, when=F['has_slaves'], id="slv"),
        state=states.Home.home,  # state is used to identify window between dialogs
    ),
    Window(
        Format("{l_link} {link}"),
        Back(Format("{l_back}")),
        state=states.Home.link,
    ),
    Window(
        Format("{l_slaves_tip}"),
        Format("{l_slaves}:\n"),
        List(
            Format("{pos}. {item[0]}"),
            items="slaves",
            page_size=20,
            id="slaves_list"
        ),
        ScrollingGroup(
            NumberedPager(scroll="slaves_list"),
            width=8,
            height=8,
            id = 'g_scr',
            hide_pager=True
        ),
        SwitchTo(Format("{l_back}"), state=states.Home.home, id="home"),
        MessageInput(slave_number_handler, content_types=[ContentType.TEXT]),
        getter=slaves_getter,
        state=states.Home.slaves,
    ),
    getter=home_getter
)