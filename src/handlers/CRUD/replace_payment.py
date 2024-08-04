from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb
from src.states.state import EditTitlePayment


@dp.callback_query_handler(Text(startswith='editPayment_'))
async def call_edit_payment(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditTitlePayment.id_payment.state)
    
    _id_payment = int(call.data.split('_')[1])
    
    async with state.proxy() as data:
        data['id_payment'] = _id_payment

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['message_new_add_title_payments'],
                                 reply_markup = await ikb.cancel_edit_payment(user[8]))


@dp.message_handler(state=EditTitlePayment.id_payment)
async def message_new_title(message: types.Message, state: FSMContext):
    payment_title = message.text

    user = await datapro.processing_select_all_info_user(message.from_user.id)

    if len(payment_title) > 20:
        payment_title = message.text[:20]

    async with state.proxy() as data:
        _id_payment = data['id_payment']
        await datapro.processing_update_payment_title(message.from_user.id, _id_payment, payment_title)

    await state.finish()
    
    await message.answer(_messages['message'][user[8]]['p2p_payment'],
                                 reply_markup = await ikb.select_all_payment_user(user[8], datapro, message.from_user.id))


@dp.callback_query_handler(text='cancel_edit_payment',  state=EditTitlePayment)
async def cancel_edit_payment(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['p2p_payment'],
                                 reply_markup = await ikb.select_all_payment_user(user[8], datapro, call.from_user.id))