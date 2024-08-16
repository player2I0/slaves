from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button, Next, Back
from aiogram_dialog.widgets.text import Const, Format

from aiogram.types import User
from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link, decode_payload

from db import User as UserDB

import states

async def home_getter(dialog_manager: DialogManager, event_from_user: User, db_user: UserDB, bot: Bot, **kwargs):
    locale = {
        "welcome": {"en": "Hello"},
        "link": {'en': "Your link: ", "ru": "Ваша ссылка: "},
        "back": {"en": "‹ Back", "ru": "‹ Назад"},
        "get_link": {"en": "Your link", "ru": "Ваша ссылка"}
    }

    if db_user.is_enslaved():
        owner = db_user.get_owner()
        locale['status'] = {'en': "You are currently a slave of " + owner.name, "ru": "Вы находитесь в рабстве. Ваш хозяин - " + owner.name}
    else:
        locale['status'] = {'en': "You are currently free", "ru": "Вы (пока что) свободны"}

    data = states.user_locale(locale, event_from_user.language_code)

    data['link'] = await create_start_link(bot, str(event_from_user.id), encode=True)

    return data

dialog = Dialog(
    Window(
        Format("{l_status}"),  # just a constant text
        #Button(Const("Useless button"), id="nothing"),  # button with text and id
        Next(Format("{l_get_link}")),
        state=states.Home.home,  # state is used to identify window between dialogs
    ),
    Window(
        Format("{l_link} {link}"),
        Back(Format("{l_back}")),
        state=states.Home.link,
    ),
    getter=home_getter
)