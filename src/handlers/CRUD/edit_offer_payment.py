from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from src.system.message_system import _messages
from src.states.state import EditOfferPayment
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb
from src.handlers.user.offers import offer as main_offer


@dp.callback_query_handler(Text(startswith='offerEditPaymentMethods_'))
async def call_edit_payment_offer(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    
    await state.set_state(EditOfferPayment.new_payment.state)

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    offer = await datapro.processing_select_offer(int(call_msg[1]))

    list_payment_id = []
    for i in offer[5].split(','):
        list_payment_id.append(int(i))

    async with state.proxy() as data:
        data['id_offer'] = int(call_msg[1])
        data['new_payment'] = list_payment_id
        data['page'] = int(call_msg[2])

    await call.message.edit_text(_messages['message'][user[8]]['select_payments_method_sell'], 
                                 reply_markup = await ikb.edit_offer_payment(user[8], call.from_user.id, offer[2], list_payment_id, datapro, call_msg[1], call_msg[2]))
    

@dp.callback_query_handler(Text(startswith='editOfferPayment_'), state=EditOfferPayment.new_payment.state)
async def call_set_offer_payment(call: types.CallbackQuery, state: FSMContext):
    payment_id = int(call.data.split('_')[1])

    async with state.proxy() as data:
        _payment_method = data.get('new_payment', [])  # Получаем текущий список способов оплаты

        if payment_id in _payment_method:
            if len(_payment_method) > 1:
                _payment_method.remove(payment_id) # Удаляем способ оплаты
    
        elif not payment_id in _payment_method:
            _payment_method.append(payment_id)  # Добавляем новый способ оплаты
    
        await state.update_data(payment_method=_payment_method)  # Обновляем состояние с новым списком способов оплаты

    async with state.proxy() as data:
        id_offer = data['id_offer']
        new_payment = data['new_payment']
        page = data['page']

    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    offer = await datapro.processing_select_offer(id_offer)
    
    try:
        await call.message.edit_text(_messages['message'][user[8]]['select_payments_method_sell'], 
                                    reply_markup = await ikb.edit_offer_payment(user[8], call.from_user.id, offer[2], new_payment, datapro, id_offer, page))
    except exceptions.MessageNotModified:
        pass


@dp.callback_query_handler(Text(startswith='saveEditOfferPayment_'), state=EditOfferPayment.new_payment.state)
async def save_edit_offer_payment(call: types.CallbackQuery, state: FSMContext):
    id_offer = int(call.data.split('_')[1])

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    async with state.proxy() as data:
        new_payment = data['new_payment']

    new_payment = ','.join(list(map(str, new_payment)))

    await datapro.processing_update_payment_offer(call.from_user.id, id_offer, new_payment)

    await state.finish()

    await call.answer(_messages['message'][user[8]]['success_edit_payment'], show_alert = False)

    await main_offer(call)