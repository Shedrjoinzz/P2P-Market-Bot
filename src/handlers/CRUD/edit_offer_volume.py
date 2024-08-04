from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from src.system.message_system import _messages
from src.states.state import EditOfferVolume
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb
from ..user.offers import offer
from src.filters.filter import one_crypto_rate, amount_balance_min_and_max


@dp.callback_query_handler(Text(startswith='offerEditVolume_'))
async def offer_edit_volume(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditOfferVolume.new_crypto_volume.state)
    call_msg = call.data.split('_')

    async with state.proxy() as data:
        data['id_offer'] = int(call_msg[1])
        data['page'] = int(call_msg[2])

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    _offer = await datapro.processing_select_offer(int(call_msg[1]))

    crypto_rate = await one_crypto_rate(_offer[1], _offer[2], datapro)

    crypto_balance = _offer[4]

    if _offer[11] == 'sell':
        crypto_balance = await datapro.prosessing_select_one_balance_user(call.from_user.id, _offer[1])
        
    currency_balance = f"{float(crypto_balance)*float(crypto_rate)}"

    
    if _offer[2] == 'USD':
        currency_balance += '$'

    if _offer[2] == 'RUB':
        currency_balance += '₽'
    
    key_message = f'message_count_ad_crypto_{_offer[11]}'

    await call.message.edit_text(_messages['message'][user[8]][key_message].format(
        _offer[1],
        _messages['message'][user[8]]['select_cryptocurrency_ad_type_message_sell'],
        crypto_balance,
        _offer[1],
        currency_balance
    ), reply_markup = await ikb.edit_offer_amount_user_max(user[8], crypto_balance, _offer[1], call_msg[1], call_msg[2], _type=_offer[11]))


@dp.callback_query_handler(Text(startswith='sellAmountAdvertisementMax_'), state=EditOfferVolume.states)
async def edit_max_volume_offer(call: types.CallbackQuery, state: FSMContext):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    async with state.proxy() as data:
        _id_offer = data['id_offer']

    _offer = await datapro.processing_select_offer(_id_offer)
    balance_user = await datapro.prosessing_select_one_balance_user(call.from_user.id, _offer[1])

    await datapro.processing_update_crypto_volume_offer(call.from_user.id, _id_offer, balance_user)

    await call.answer(_messages['message'][user[8]]['success_edit_volume'], show_alert=False)
    await state.finish()
    await offer(call)


@dp.message_handler(state=EditOfferVolume.new_crypto_volume.state)
async def message_new_crypto_volume_offer(message: types.Message, state: FSMContext):
    user = await datapro.processing_select_all_info_user(message.from_user.id)


    async with state.proxy() as data:
        _id_offer = data['id_offer']
        page = data['page']

    _offer = await datapro.processing_select_offer(_id_offer)

    balance_user = await datapro.prosessing_select_one_balance_user(message.from_user.id, _offer[1])
    
    crypto_rate = await one_crypto_rate(_offer[1], _offer[2], datapro)

    min_crypto_count_ad, min_currency_count_ad = await amount_balance_min_and_max(_offer[1], user[7], crypto_rate)

    try:
        message_amount = float(message.text)
        if _offer[11] == 'sell':
            if message_amount > balance_user:
                return await message.answer(_messages['message'][user[8]]['error_message_total_balance_max'].format(balance_user, _offer[1]))

            if message_amount < min_crypto_count_ad:                
                return await message.answer(_messages['message'][user[8]]['error_message_total_balance_min'].format(min_crypto_count_ad, _offer[1], min_currency_count_ad))
    except Exception:
        return await message.answer(_messages['message'][user[8]]['error_ad_crypto_rate'])
    
    await datapro.processing_update_crypto_volume_offer(message.from_user.id, _id_offer, message_amount)
 
    await message.answer(_messages['message'][user[8]]['success_edit_volume'],
                         reply_markup = await ikb.back_to_offer(user[8], _id_offer, page))