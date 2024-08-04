from aiogram import types

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text='payment_currency')
async def p2p_payment_currency(call: types.CallbackQuery):    
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    currency_market = await datapro.processing_select_user_p2p_market(call.from_user.id)
    
    await call.message.edit_text(_messages['message'][user[8]]['p2p_currency_payment_message'],
                                 reply_markup = await ikb.market_payment_currency(user[8], currency_market[1]))