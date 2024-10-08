from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, User, TelegramObject

class MessageMiddleware(BaseMiddleware):
    def __init__(self, users) -> None:
        self.users = users

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        #print(list(self.users.select().where(self.users.id == event.from_user.id)))
        print(event)
        #print(event.from_user)
        event_user = None

        if event.message is not None:
            event_user = event.message.from_user
        elif hasattr(event, 'from_user'):
            event_user = event.from_user
        
        if event_user is not None:
            usr = self.users(id = event_user.id)

            if not self.users.select().where(self.users.id == event_user.id).exists():
                usr_name = event_user.first_name

                if event_user.last_name is not None:
                    usr_name += ' ' +  event_user.last_name

                usr = self.users(id = event_user.id, name = usr_name)
                usr.save(force_insert=True)
            else:
                usr = self.users.get(self.users.id == event_user.id)

            #return {'db_user': usr}
            data['db_user'] = usr
        #print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
        
        #data['db_user'] = self.users.get(self.users.id == 1321983182)
        return await handler(event, data)