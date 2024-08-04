from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from src.system.message_system import _messages
from src.states.state import EditOfferTime
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb
from src.handlers.user.offers import offer as main_offer


@dp.callback_query_handler(Text(startswith='offerEditPaymentTime_'))
async def offer_edit_payment_time(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')

    await state.set_state(EditOfferTime.new_time.state)

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    offer = await datapro.processing_select_offer(int(call_msg[1]))

    async with state.proxy() as data:
        data['id_offer'] = int(call_msg[1])
        data['new_time'] = offer[6]
        data['page'] = int(call_msg[2])

    _time = f'newTimerDeals_{offer[6]}'

    await call.message.edit_text(_messages['message'][user[8]]['select_time_deals'],
                                 reply_markup = await ikb.edit_offer_time(user[8], _time, int(call_msg[1]), int(call_msg[2])))


@dp.callback_query_handler(Text(startswith='newTimerDeals_'), state=EditOfferTime.new_time.state)
async def set_new_timer_deals(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')


    async with state.proxy() as data:
        id_offer = data['id_offer']
        data['new_time'] = int(call_msg[1])
        page = data['page']

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    try:
        await call.message.edit_text(_messages['message'][user[8]]['select_time_deals'],
                                    reply_markup = await ikb.edit_offer_time(user[8], call.data, id_offer, page))
    except exceptions.MessageNotModified:
        pass


@dp.callback_query_handler(Text(startswith='saveEditOfferTime_'), state=EditOfferTime.new_time.state)
async def save_edit_offer_time(call: types.CallbackQuery, state: FSMContext):
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    async with state.proxy() as data:
        id_offer = data['id_offer']
        new_time = data['new_time']

    await datapro.processing_update_time_offer(call.from_user.id, id_offer, new_time)

    await call.answer(_messages['message'][user[8]]['success_edit_payment'], show_alert = False)

    await state.finish()
    
    await main_offer(call)    











