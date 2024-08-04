from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp

from src.processing import data_processing as datapro
from src.system.message_system import _messages
from src.system.ban_system import is_ban_user
from src.handlers.keyboards import inline_keyboards as ikb



@dp.callback_query_handler(Text(startswith='deposit_'))
async def selection_deposit(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    call_message = call.data.split('_')
    # print(call_message)
    await call.message.edit_text(_messages['message'][user[8]]['war_deposit_crypto'].format(call_message[1]),
                                 reply_markup=await ikb.back_to_menu(user[8]))


@dp.callback_query_handler(text='deposit')
async def deposit(call: types.CallbackQuery):
    is_user_ban = await is_ban_user(call.from_user.id)
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    if is_user_ban == True:
        info_ban = await datapro.processing_select_info_ban_user(call.from_user.id)
        return await call.message.answer(_messages['message'][user[8]]['ban']+f'\n\n<b>Description ban:</b>\n<i>-{info_ban[1]}</i>')

    await call.message.edit_text(_messages['message'][user[8]]['selection_deposit_message'],
                                 reply_markup = await ikb.crypto_deposit(lang_code=user[8], datapro=datapro))
