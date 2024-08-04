from aiogram import types
from aiogram.dispatcher.filters import Text

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text="currency_bot")
async def setting_user(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)    

    await call.message.edit_text(_messages['message'][user[8]]['select_currency_bot'],
                                 reply_markup = await ikb.select_currency_bot(user[8], user[7], 'Bot', 'setting'))


@dp.callback_query_handler(Text(startswith="selectCurrencyBot_"))
async def set_currency_bot(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    currency = call.data.split('_')[1]

    await datapro.processing_update_currency_bot(call.from_user.id, currency)
    
    await call.message.edit_text(_messages['message'][user[8]]['setting'].format(user[1], user[2], currency.upper()),
                                 reply_markup = await ikb.setting_menu(user[8], currency.upper()))