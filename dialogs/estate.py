import re

from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Next, Back, SwitchTo, NumberedPager, ScrollingGroup, Cancel, Start
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format, List

from aiogram.types import User, ContentType, Message, CallbackQuery
from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link, decode_payload

from magic_filter import F

from db import User as UserDB
from db import Estate

import states

async def estate_manager_getter(dialog_manager: DialogManager, event_from_user: User, bot: Bot, **kwargs):
    dialog_manager.show_mode = ShowMode.EDIT
    db_user = UserDB.get(UserDB.id == event_from_user.id)
    data = {}

    locale = {
        "back": {"en": "‹ Back", "ru": "‹ Назад"},
        "title": {"en": "Send a message with estate's index to know more.\n<b>Your estate:</b>", "ru": "Отправьте сообщение с номером имения, чтобы узнать о нём больше.\n<b>Ваши имения:</b>"},
        "shop_title": {"en": "Buy estate", "ru": "Покупка имения"},
        "buy": {"en": "Buy estate", "ru": "Купить имения"},
        "no_estate": {"en": "You don't have any estate. You can buy one.", "ru": "У вас нет имений, но вы можете купить одно."}
    }

    data = data | states.user_locale(locale, event_from_user.language_code) #merge two dicts together (python 3.9+)

    data['popup'] = dialog_manager.start_data.get('popup', False)

    if len(db_user.estates) > 0:
        data['has_estate'] = True
    else:
        data['has_estate'] = False

    return data

async def estate_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    db_user = UserDB.get(UserDB.id == event_from_user.id)
    l = []
    i = 0

    for estate_id in db_user.estates:
        estate = Estate.get(Estate.id == estate_id)

        l.append((estate.to_string()[db_user.lang], i))
        
        i += 1

    return {'estates': l}

async def estate_shop_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    db_user = UserDB.get(UserDB.id == event_from_user.id)

    return states.user_locale({"back": {"en": "‹ Back", "ru": "‹ Назад"}}, event_from_user.language_code)

manager = Dialog(
    Window(
        Format('{l_title}\n'),
        Format('{l_no_estate}', when=~F['has_estate']),
        List(
            Format("{pos}. {item[0]}"),
            items="estates",
            page_size=20,
            id="estates_list",
            when=F['has_estate']
        ),
        ScrollingGroup(
            NumberedPager(scroll="estates_list"),
            width=8,
            height=8,
            id = 'g_scr',
            hide_pager=True,
            when=F['has_estate']
        ),
        Start(Format("{l_buy}"), state=states.EstateManager.shop, id="b"),
        Cancel(Format('{l_back}'), when=F['popup']),
        state=states.EstateManager.estate_list,
        getter=estate_getter
    ),
    getter=estate_manager_getter
)

shop = Dialog(
    Window(
        Format('<b>{l_shop_title}</b>\n'),
        Start(Format("{l_back}"), state=states.EstateManager.estate_list, id="b"),
        state=states.EstateManager.shop
    ),
    getter=estate_shop_getter
)