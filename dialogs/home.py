from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from aiogram.types import User

from db import User as UserDB

import states

async def home_getter(dialog_manager: DialogManager, event_from_user: User, db_user: UserDB, **kwargs):
    return states.user_locale({
        "lang_welcome": {"en": "Hello"}
    }, event_from_user.language_code)

dialog = Dialog(
    Window(
        Format("{lang_welcome}"),  # just a constant text
        Button(Const("Useless button"), id="nothing"),  # button with text and id
        state=states.Home.home,  # state is used to identify window between dialogs
    ),
    getter=home_getter
)