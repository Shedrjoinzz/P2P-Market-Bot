from aiogram import types
from aiogram.dispatcher.filters import Text

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text='payment_method')
async def payment_method(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['p2p_payment'],
                                 reply_markup = await ikb.select_all_payment_user(user[8], datapro, call.from_user.id))
    

@dp.callback_query_handler(Text(startswith='givePayment_'))
async def call_give_payment(call: types.CallbackQuery):
    _id_payment = call.data.split('_')[1]

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    payment_info = await datapro.processing_select_payment_info(call.from_user.id, int(_id_payment))

    title = payment_info[0]
    if title is None:
        title = _messages['message'][user[8]]['not_specific_title_payment']

    await call.message.edit_text(_messages['message'][user[8]]['payment_info'].format(
        title,
        payment_info[1],
        payment_info[2],
        payment_info[3],
        payment_info[4]), reply_markup = await ikb.menu_payment_nav(user[8], _id_payment))