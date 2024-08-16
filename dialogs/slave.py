import re

from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Next, Back, SwitchTo, NumberedPager, ScrollingGroup
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format, List

from aiogram.types import User, ContentType, Message, CallbackQuery
from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link, decode_payload

from magic_filter import F

from db import User as UserDB

import states

async def slave_manager_getter(dialog_manager: DialogManager, event_from_user: User, bot: Bot, **kwargs):
    dialog_manager.show_mode = ShowMode.EDIT
    db_user = UserDB.get(UserDB.id == event_from_user.id)
    data = {}

    locale = {
        "back": {"en": "‹ Back", "ru": "‹ Назад"},
    }

    data = data | states.user_locale(locale, event_from_user.language_code) #merge two dicts together (python 3.9+)

    slave = UserDB.get(UserDB.id == dialog_manager.start_data['slave_id'])
    data['slave_id'] = dialog_manager.start_data['slave_id']
    data['slave_name'] = slave.name
    data['popup'] = dialog_manager.start_data.get('popup', False)

    return data

async def slave_go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()

manager = Dialog(
    Window(
        Format('<b>{slave_name}</b>'),
        Button(Format('{l_back}'), when=F['popup'], on_click=slave_go_back, id='b'),
        state=states.SlaveManager.info
    ),
    getter=slave_manager_getter
)