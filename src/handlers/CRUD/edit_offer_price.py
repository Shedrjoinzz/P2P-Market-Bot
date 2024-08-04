from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from src.system.message_system import _messages
from src.states.state import EditOfferPrice
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb
from ..user.offers import offer as main_offer


@dp.callback_query_handler(Text(startswith='newCryptoRateFixed_'), state=EditOfferPrice.states)
@dp.callback_query_handler(Text(startswith='offerEditPrice_'))
async def call(call: types.CallbackQuery, state: FSMContext):
    id_offer = int(call.data.split('_')[1])

    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    offer = await datapro.processing_select_offer(id_offer)

    await state.set_state(EditOfferPrice.new_crypto_rate.state)

    _type_add = offer[11]

    _crypto = offer[1]

    if offer[2] == 'USD':
        _crypto = offer[1]+'USDT'

    crypto_rate = 0

    _crypto_rate = offer[1]+offer[2]


    if offer[2].lower() == "usd" and offer[1] == "USDT":
        crypto_rate = 1

    if offer[2].lower() == "usdt" and _crypto != "USDT" or offer[2].lower() == "rub" or offer[2].lower() != "usdt" and _crypto == "USDT": 
        crypto_rate = await datapro.processing_select_one_crypto_rates(_crypto_rate)

    async with state.proxy() as data:
        data['id_offer'] = offer[0]
        data['new_crypto_rate'] = crypto_rate
        data['page'] = call.data.split('_')[2]

    if offer[2].lower() == 'usd':
        crypto_rate = f'${crypto_rate}'
    if offer[2].lower() == 'rub':
        crypto_rate = f'{crypto_rate}₽'

    try:
        await call.message.edit_text(_messages['message'][user[8]]['select_currency_ad_rate_message'].format(
            offer[2],
            _messages['message'][user[8]][f'select_cryptocurrency_ad_type_message_{_type_add}'],
            offer[1],
            crypto_rate,
            offer[1],
            crypto_rate
        ), reply_markup = await ikb.edit_offer_crypto_rate(user[8], 'title_fixed_select', offer[0], int(call.data.split('_')[2])))
    except:
        pass


@dp.message_handler(state=EditOfferPrice.new_crypto_rate.state) # 4
async def advertisement_user_cryptocurrency_rate_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        id_offer = data['id_offer']
        page = data['page']

    offer = await datapro.processing_select_offer(id_offer)

    _type_add = offer[11]

    call_message = offer[2]

    _crypto = offer[1]

    user = await datapro.processing_select_all_info_user(message.from_user.id)

    crypto_rates = _crypto + call_message.replace("USD", "USDT") # call_message -> RUB or USD
    crypto_rate = 1
    _call_message = call_message.lower()

    if _call_message == "usd" and _crypto == "USDT":
        crypto_rate = 1
    if _call_message == "usd" and _crypto != "USDT" or _call_message == "rub" or _call_message != "usd" and _crypto == "USDT":
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)
    
    crypto_rate_devision = crypto_rate / 2
    min_crypto_rate = crypto_rate - crypto_rate_devision
    max_crypto_rate = crypto_rate + crypto_rate_devision
    min_crypto_rate_symbol_currency = ''
    max_crypto_rate_symbol_currency = ''

    try:
        user_crypto_rate = float(message.text)
        if _call_message == 'usd':
            min_crypto_rate_symbol_currency = f'${min_crypto_rate:.2f}'
            max_crypto_rate_symbol_currency = f'${max_crypto_rate:.2f}'

        if _call_message == 'rub':
            min_crypto_rate_symbol_currency = f'{min_crypto_rate:.2f}₽'
            max_crypto_rate_symbol_currency = f'{max_crypto_rate:.2f}₽'

        if user_crypto_rate < min_crypto_rate or user_crypto_rate > max_crypto_rate:
            return await message.answer(_messages['message'][user[8]]['message_ad_min_and_max_crypto_rate'].format(
                min_crypto_rate_symbol_currency,
                max_crypto_rate_symbol_currency
            ))

    except:
        return await message.answer(_messages['message'][user[8]]['error_ad_crypto_rate'])

    async with state.proxy() as data:
        data['new_crypto_rate'] = user_crypto_rate

    if _call_message == 'usd':
        user_crypto_rate = f'${user_crypto_rate}'
        crypto_rate = f'${crypto_rate}'
    if _call_message == 'rub':
        user_crypto_rate = f'{user_crypto_rate}₽'
        crypto_rate = f'{crypto_rate}₽'

    
    await message.answer(_messages['message'][user[8]]['select_currency_ad_rate_message'].format(
        call_message,
        _messages['message'][user[8]][f'select_cryptocurrency_ad_type_message_{_type_add}'],
        _crypto,
        crypto_rate,
        _crypto,
        user_crypto_rate
    ), reply_markup = await ikb.edit_offer_crypto_rate(user[8], False, id_offer, page))


@dp.callback_query_handler(Text(startswith='saveEditPrice_'), state=EditOfferPrice.new_crypto_rate.state)
async def call_save_edit_price(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id_offer = data['id_offer']
        new_crypto_rate = data['new_crypto_rate']

    await datapro.processing_update_crypto_rates_offer(call.from_user.id, id_offer, new_crypto_rate)
    await state.finish()
    await main_offer(call)