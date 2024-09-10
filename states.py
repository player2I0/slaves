from aiogram.filters.state import StatesGroup, State
from aiogram.types import User, ContentType, Message, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Next, Back, SwitchTo, NumberedPager, ScrollingGroup

def user_locale(data, locale):
    n = {}

    for key in data:
        if locale in data[key]:
            n['l_' + key] = data[key][locale]
        else:
            n['l_' + key] = data[key]['en']
    
    return n
    
async def dialog_go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()

class Home(StatesGroup):
    home = State()
    link = State()
    slaves = State()


class SlaveManager(StatesGroup):
    info = State()


class EstateManager(StatesGroup):
    estate_list = State()
    shop = State()