from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled, MessageToEditNotFound, MessageNotModified
from aiogram.dispatcher.handler import CancelHandler, current_handler

import asyncio
from datetime import datetime

from src.processing import data_processing as datapro
from src.system.message_system import _messages
from src.system.ban_system import is_ban_user
from loader import dp


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=2, key_prefix='antiflood'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()
    
    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):

        handler = current_handler.get()

        dispatcher = dp.get_current()
        
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        user = await datapro.processing_select_all_info_user(call.from_user.id)
        try:
            is_user_ban = await is_ban_user(call.from_user.id)

            if is_user_ban == True:
                info_ban = await datapro.processing_select_info_ban_user(call.from_user.id)
                print(info_ban[2] == datetime.now().date())
                if info_ban[2] == datetime.now().date():
                    await datapro.processing_unban_user(call.from_user.id)

                await call.message.edit_text(_messages['message'][user[8]]['ban']+f'\n\n<b>Description ban:</b>\n<i>-{info_ban[1]}</i>')
                raise CancelHandler()

            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
          
            await self.message_throttled(call, t, user[8])

            raise CancelHandler()
        except MessageToEditNotFound:
            pass
        except MessageNotModified:
            print('edit not found')
            pass


    async def message_throttled(self, call: types.CallbackQuery, throttled: Throttled, lang_code: str):

        handler = current_handler.get()
        dispatcher = dp.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 5:
            await call.answer(_messages['message'][lang_code]['time_take_user'], show_alert=True)

        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)

        if thr.exceeded_count == throttled.exceeded_count:
            pass
