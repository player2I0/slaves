from aiogram.filters.state import StatesGroup, State

def user_locale(data, locale):
    n = {}

    for key in data:
        if locale in data[key]:
            n['l_' + key] = data[key][locale]
        else:
            n['l_' + key] = data[key]['en']
    
    return n

class Home(StatesGroup):
    home = State()
    link = State()
    slaves = State()