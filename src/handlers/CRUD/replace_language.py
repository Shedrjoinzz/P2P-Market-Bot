from aiogram import types
from aiogram.dispatcher.filters import Text

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text="bot_language")
async def replace_language_bot(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    await call.message.edit_text(_messages['message'][user[8]]['select_language_bot'],
                                 reply_markup=await ikb.select_language_bot(user[8]))
    

@dp.callback_query_handler(Text(startswith="selectLanguageBot_"))
async def set_language_bot(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    lang_code = call.data.split('_')[1]

    await datapro.processing_update_language_bot(id_user=call.from_user.id, lang_code=lang_code)
    
    await call.message.edit_text(_messages['message'][lang_code]['old_user'],
                                 reply_markup= await ikb.main_menu(lang_code=lang_code))
