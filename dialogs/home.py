from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

import states

dialog = Dialog(
    Window(
        Const("Hello, unknown person"),  # just a constant text
        Button(Const("Useless button"), id="nothing"),  # button with text and id
        state=states.Home.home,  # state is used to identify window between dialogs
    )
)