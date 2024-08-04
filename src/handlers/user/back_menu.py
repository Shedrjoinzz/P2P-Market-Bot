from aiogram import types

from loader import dp
from src.handlers.keyboards import inline_keyboards as ikb
from src.system.message_system import _messages
from src.processing import data_processing as datapro


@dp.callback_query_handler(text="back_menu")
async def back_main_menu(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['old_user'],
                        reply_markup= await ikb.main_menu(lang_code=user[8]))