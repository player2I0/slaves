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

async def slave_manager_getter(dialog_manager: DialogManager, event_from_user: User, bot: Bot, **kwargs):
    db_user = UserDB.get(UserDB.id == event_from_user.id)
    data = {}

    locale = {
        "back": {"en": "‹ Back", "ru": "‹ Назад"},
    }

    data = data | states.user_locale(locale, event_from_user.language_code) #merge two dicts together (python 3.9+)

    slave = UserDB.get(UserDB.id == dialog_manager.start_data['slave_id'])
    data['slave_id'] = dialog_manager.start_data['slave_id']
    data['slave_name'] = slave.name

    return data

manager = Dialog(
    Window(
        Format('<b>{slave_name}</b>'),
        Back(Format('{l_back}'), when=F['popup']),
        state=states.SlaveManager.info
    ),
    getter=slave_manager_getter
)