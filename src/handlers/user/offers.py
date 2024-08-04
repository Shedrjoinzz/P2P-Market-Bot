from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp
from src.filters.filter import filter_decimal
from src.states.state import EditOfferPrice, EditOfferVolume, EditOfferLimit, EditOfferPayment, EditOfferTime
from src.handlers.keyboards import inline_keyboards as ikb
from src.system.message_system import _messages
from src.processing import data_processing as datapro


@dp.callback_query_handler(Text(startswith='myOffersPage_'))
async def my_offers(call: types.CallbackQuery):
    page = int(call.data.split('_')[1])
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['offers_manager'],
                                 reply_markup = await ikb.offers(user[8], datapro, call.from_user.id, page))


@dp.callback_query_handler(Text(startswith='BackFromEditOffer_'), state=[EditOfferPrice, EditOfferVolume, EditOfferLimit, EditOfferPayment, EditOfferTime])
@dp.callback_query_handler(Text(startswith='EditOfferSave_'), state=EditOfferPrice)
@dp.callback_query_handler(Text(startswith='openOfferEdit_'))
async def open_offer_edit(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await offer(call)


async def offer(call: types.CallbackQuery):
    call_status_offer = call.data.split('_')

    id_offer = int(call.data.split('_')[1])

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    offer = await datapro.processing_select_offer(id_offer)

    label_pay = ''
    
    for index, payments in enumerate(offer[5].split(',')):
        payment = await datapro.processing_select_payment_info(call.from_user.id, int(payments))
        label_pay += f'{index+1}) {payment[3]} *{payment[4][-4:]}\n'

    key_method_time =  'time_min'
    if offer[6] == 1:
        key_method_time = 'time_hour'
    label_time = _messages['button'][user[8]][key_method_time].format(offer[6])


    status_offer = offer[8]

    json_key_method_active = 'active_ad'

    page = call_status_offer[2]

    if len(call_status_offer) > 3:
        page = call_status_offer[3]
        if call_status_offer[2] == 'True':
            status_offer = False

        if call_status_offer[2] == 'False':
            status_offer = True

        await datapro.processing_update_status_offer(call.from_user.id, offer[0], status_offer)

    if status_offer == False:
        json_key_method_active = 'deactive_ad'


    label_isActive_advertisement = _messages['message'][user[8]][json_key_method_active]


    valume = await filter_decimal(offer[4])

    type_add_message = _messages['button'][user[8]][offer[11]]

    try:
        await call.message.edit_text(_messages['message'][user[8]]['offer_info'].format(
            offer[0],
            offer[0],
            type_add_message,
            offer[1],
            offer[2],
            offer[3],
            offer[2],
            valume,
            offer[1],
            offer[12],
            offer[2],
            offer[13],
            offer[2],
            label_pay,
            label_time,
            label_isActive_advertisement
        ), reply_markup = await ikb.view_offer(user[8], status_offer, offer[0], page))
    except:
        pass