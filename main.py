import datetime

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
#from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import BaseEventIsolation
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.client.default import DefaultBotProperties

from aiogram_dialog import DialogManager, StartMode, setup_dialogs

import db
import middlewares
import dialogs
import states

#print(db.db)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.environ.get("TOKEN"), default=DefaultBotProperties(parse_mode='HTML'))
# Диспетчер

#STORAGE = RedisStorage.from_url('redis://localhost:6379', key_builder=DefaultKeyBuilder(with_bot_id=True, 
#                                                                                        with_destiny=True))

STORAGE = MemoryStorage()
dp = Dispatcher(storage=STORAGE)

dialogs.setup(dp)
setup_dialogs(dp)

#dp.update.middleware(middlewares.MessageMiddleware(db.User))

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, dialog_manager: DialogManager, command: CommandObject):
    global db

    db_user = None

    if not db.User.select().where(db.User.id == message.from_user.id).exists():
        usr_name = message.from_user.first_name

        if message.from_user.last_name is not None:
            usr_name += ' ' +  message.from_user.last_name

        db_user = db.User(id = message.from_user.id, name = usr_name, lang = message.from_user.language_code, enslaved_date = datetime.datetime.today())
        db_user.save(force_insert=True)
    else:
        db_user = db.User.get(db.User.id == message.from_user.id)

    #print(command.args)
    #print(db_user)

    if command.args is not None and not db_user.is_enslaved():
        id = int(decode_payload(command.args))
        owner: db.User = db.User.get_or_none(db.User.id == id)
        #owner = self.users.select().where(self.users.id == event.from_user.id)

        if owner is not None and not owner.is_enslaved() and owner.id != db_user.id:
            db_user.enslave(owner)
            print(states.user_locale({'msg': {'en': '<b>' + db_user.name + '</b> got enslaved via your link!', 'ru': '<b>' + db_user.name + '</b> стал вашим рабом через ссылку!'}}, owner.lang))
            await bot.send_message(chat_id=owner.id, text=states.user_locale({'msg': {'en': '<b>' + db_user.name + '</b> got enslaved via your link!', 'ru': '<b>' + db_user.name + '</b> стал вашим рабом через ссылку!'}}, owner.lang)['l_msg'], reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="❌", callback_data='close')]]))

    #await message.answer("Hello!")
    await dialog_manager.start(states.Home.home, mode=StartMode.RESET_STACK)

@dp.callback_query(F.data == "close")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.delete()

@dp.message(Command("link"))
async def cmd_start(message: types.Message, dialog_manager: DialogManager, command: CommandObject):
    await message.answer(await create_start_link(bot, str(message.from_user.id), encode=True))

@dp.message(Command("slave"))
async def cmd_start(message: types.Message, dialog_manager: DialogManager):
    global db
    db_user = db.User.get(db.User.id == message.from_user.id)

    #print(db_user.id)

    #await message.answer("Hello!")
    #await dialog_manager.start(states.Home.home, mode=StartMode.RESET_STACK)
    db.User.get(db.User.id == 784169759).enslave(db_user)
    print(db_user.slaves)

# Запуск процесса поллинга новых апдейтов
async def main():
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
