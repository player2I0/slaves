import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import DialogManager, StartMode, setup_dialogs

import db
import middlewares
import dialogs
import states

#print(db.db)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.environ.get("TOKEN"))
# Диспетчер

#STORAGE = RedisStorage.from_url('redis://localhost:6379', key_builder=DefaultKeyBuilder(with_bot_id=True, 
#                                                                                        with_destiny=True))

STORAGE = MemoryStorage()
dp = Dispatcher(storage=STORAGE)

dialogs.setup(dp)
setup_dialogs(dp)

dp.message.middleware(middlewares.MessageMiddleware(db.User))
dp.callback_query.middleware(middlewares.MessageMiddleware(db.User))

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, db_user: db.User, dialog_manager: DialogManager):
    #global db

    #print(db_user.id)

    #await message.answer("Hello!")
    await dialog_manager.start(states.Home.home, mode=StartMode.RESET_STACK)

# Запуск процесса поллинга новых апдейтов
async def main():
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
