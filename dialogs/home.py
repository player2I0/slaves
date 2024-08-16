from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button, Next, Back, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, List

from aiogram.types import User
from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link, decode_payload

from magic_filter import F

from db import User as UserDB

import states

async def home_getter(dialog_manager: DialogManager, event_from_user: User, db_user: UserDB, bot: Bot, **kwargs):
    #print('get!')
    data = {'has_slaves': False}

    locale = {
        "welcome": {"en": "Hello"},
        "link": {'en': "Your link: ", "ru": "Ваша ссылка: "},
        "back": {"en": "‹ Back", "ru": "‹ Назад"},
        "get_link": {"en": "Your link", "ru": "Ваша ссылка"},
        "slaves": {"en": "Your slaves", "ru": "Ваши рабы"}
    }

    if db_user.is_enslaved():
        owner = db_user.get_owner()
        locale['status'] = {'en': "You are currently a slave of " + owner.name, "ru": "Вы находитесь в рабстве. Ваш хозяин - " + owner.name}
    else:
        locale['status'] = {'en': "You are currently free", "ru": "Вы (пока что) свободны"}

        slaves = list(UserDB.select().where(UserDB.ownerId == db_user.id))
        data['slaves'] = [(f"{slaves[i].name}", i) for i in range(len(slaves))]

        if len(slaves) > 0:
            data['has_slaves'] = True

    data = data | states.user_locale(locale, event_from_user.language_code) #merge two dicts together (python 3.9+)

    data['link'] = await create_start_link(bot, str(event_from_user.id), encode=True)

    return data

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
        Format("{l_slaves}:"),
        SwitchTo(Format("{l_back}"), state=states.Home.home, id="home"),
        List(
            Format("{pos}. {item[0]}"),
            items="slaves",
            page_size=30
        ),
        state=states.Home.slaves,
    ),
    getter=home_getter
)