from aiogram import types
from aiogram.dispatcher.filters import Text

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text="currency_market")
async def setting_user(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)    

    currency = await datapro.processing_select_user_p2p_market(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['select_p2p_currency'],
                                 reply_markup = await ikb.select_currency_bot(user[8], currency[1], 'Market', 'payment_currency'))


@dp.callback_query_handler(Text(startswith="selectCurrencyMarket_"))
async def set_currency_bot(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    currency = call.data.split('_')[1]

    await datapro.processing_update_p2p_currency(call.from_user.id, currency.upper())
    
    await call.message.edit_text(_messages['message'][user[8]]['p2p_currency_payment_message'],
                                 reply_markup = await ikb.market_payment_currency(user[8], currency.upper()))