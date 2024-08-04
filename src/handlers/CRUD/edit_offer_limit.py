from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from src.system.message_system import _messages
from src.states.state import EditOfferLimit
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb
from src.filters.filter import limits, one_crypto_rate


@dp.callback_query_handler(Text(startswith='offerEditLimits_'))
async def advertisement_limit(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditOfferLimit.new_limit_deals.state)
    call_msg = call.data.split('_')

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    offer = await datapro.processing_select_offer(int(call_msg[1]))

    async with state.proxy() as data:
        data['id_offer'] = int(call_msg[1])
        data['page'] = int(call_msg[2])

    _currency = offer[2]
    _crypto = offer[1]

    crypto_rate = await one_crypto_rate(_crypto, _currency, datapro)

    message_amount =  offer[4]

    min_limit, max_limit, message_amount_currency, _amount_currency = await limits(_currency, _crypto, crypto_rate, message_amount)

    await call.message.edit_text(_messages['message'][user[8]]['message_limit_ad_orders'].format(
        _currency,
        min_limit,
        _amount_currency,
        min_limit,
        max_limit,
        message_amount,
        _crypto,
        message_amount_currency,
        min_limit,
        _currency,
        max_limit,
        _currency
    ), reply_markup = await ikb.edit_offer_limit(user[8], offer[12], _amount_currency, max_limit, call_msg[1], call_msg[2]))


@dp.callback_query_handler(Text(startswith='EditOfferLimit_'), state=EditOfferLimit.states)
async def call_edit_limit(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    async with state.proxy() as data:
        id_offer = data['id_offer']
        page = data['page']

    await datapro.processing_update_limit_offer(call.from_user.id, id_offer, float(call_msg[1]), float(call_msg[2]))
    
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['success_edit_limit'], 
                                 reply_markup = await ikb.back_to_offer(user[8], id_offer, page))


@dp.message_handler(state=EditOfferLimit.new_limit_deals.state)
async def advertisement_limit_orders(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_offer = data['id_offer']
        page = data['page']

    offer = await datapro.processing_select_offer(id_offer)

    _currency = offer[2]
    _crypto = offer[1]

    user = await datapro.processing_select_all_info_user(message.from_user.id)

    crypto_rate = await one_crypto_rate(_crypto, _currency, datapro)
    
    message_amount =  await datapro.prosessing_select_one_balance_user(message.from_user.id, _crypto)

    try:
        user_limit = message.text.split('-')

        min_limit, max_limit, message_amount_currency, _amount_currency = await limits(_currency, _crypto, crypto_rate, message_amount)        

        if min_limit > float(user_limit[0]):
            return await message.answer(_messages['message'][user[8]]['error_min_limit'].format(
                min_limit,
                _currency
            ))

        elif float(user_limit[0]) > float(user_limit[1]) or min_limit > float(user_limit[1]):
            return await message.answer(_messages['message'][user[8]]['error_min_max_limit'])

        elif max_limit < float(user_limit[1]):
            return await message.answer(_messages['message'][user[8]]['error_max_limit'].format(
                max_limit,
                _currency
            ))

    except:
        return await message.answer(_messages['message'][user[8]]['error_ad_limit'].format(
            _currency
        ))
    
    await datapro.processing_update_limit_offer(message.from_user.id, id_offer, float(user_limit[0]), float(user_limit[1]))
    
    await message.answer(_messages['message'][user[8]]['success_edit_limit'], 
                                 reply_markup = await ikb.back_to_offer(user[8], id_offer, page))