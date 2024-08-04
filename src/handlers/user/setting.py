from aiogram import types

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text="setting")
async def setting_user(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    await call.message.edit_text(_messages['message'][user[8]]['setting'].format(user[1], user[2], user[7].upper()),
                                 reply_markup = await ikb.setting_menu(user[8], user[7].upper()))