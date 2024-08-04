from aiogram import types
from aiogram.dispatcher.filters import Text

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(Text(startswith='deletePayment_'))
async def call_edit_payment(call: types.CallbackQuery):
    _id_payment = call.data.split('_')[1]
    
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    await call.message.edit_text(_messages['message'][user[8]]['message_delete_payment'],
                                 reply_markup = await ikb.is_delete_payment(user[8], _id_payment))


@dp.callback_query_handler(Text(startswith='yesDelete_'))
async def yes_delete(call: types.CallbackQuery):
    _id_payment = call.data.split('_')[1]

    user = await datapro.processing_select_all_info_user(call.from_user.id)
    await datapro.processing_delete_payment(call.from_user.id, int(_id_payment))

    await call.answer(_messages['message'][user[8]]['alert_success_delete_payment'], show_alert=False)

    await call.message.edit_text(_messages['message'][user[8]]['p2p_payment'],
                                 reply_markup = await ikb.select_all_payment_user(user[8], datapro, call.from_user.id)) 