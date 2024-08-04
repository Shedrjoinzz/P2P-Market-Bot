from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import exceptions

from datetime import datetime


from loader import dp
from src.handlers.keyboards import inline_keyboards as ikb
from src.system.message_system import _messages
from src.processing import data_processing as datapro
from src.filters.filter import amount_balance_min_and_max, limits
from src.states.state import AdvertisementState


@dp.callback_query_handler(text="create_offer") # 1
async def advertisement_type(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    offer_volume = await datapro.processing_select_advertisement(call.from_user.id)

    if offer_volume is not None and len(offer_volume) >= 15:
            return await call.answer(_messages['message'][user[8]]['max_offer'], show_alert=True)

    await call.message.edit_text(_messages['message'][user[8]]['select_type_ad'],
                                 reply_markup = await ikb.select_create_advertisement_type(user[8]))


@dp.callback_query_handler(Text(startswith='createAdvertisement_')) # 2
async def advertisement_cryptoCurrency(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.id_user.state)
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    call_message = call.data.split("_")[1]

    await call.message.edit_text(_messages['message'][user[8]]['select_cryptocurrency_ad'].format(
        _messages['message'][user[8]][f'select_cryptocurrency_ad_type_message_{call_message}']
    ), reply_markup = await ikb.select_create_advertisement_cryptocurrency(user[8], datapro, call_message))


@dp.callback_query_handler(Text(startswith='selectAdvertisementCryptocurrency_'), state=AdvertisementState.id_user.state) # 4
async def advertisement_Currency(call: types.CallbackQuery, state: FSMContext):
    call_message = call.data.split('_')
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    crypto_rates = call_message[1] + user[7].upper().replace("USD", "USDT")

    crypto_rate = 1
    if user[7] == "usd" and call_message[1] != "USDT" or user[7] == "rub" or user[7] != "usd" and call_message[1] == "USDT":
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)

    min_crypto_count_ad, min_currency_count_ad = await amount_balance_min_and_max(call_message[1], user[7], crypto_rate)

    if call_message[1] == "USDT":
        min_crypto_count_ad = 1


    balance_user = await datapro.prosessing_select_one_balance_user(call.from_user.id, call_message[1])
    if balance_user is None:
        balance_user = 0

    if float(balance_user) < min_crypto_count_ad and call_message[2] == 'sell':
        await state.finish()
        await call.message.edit_text(_messages['message'][user[8]]['select_type_ad'],
                                 reply_markup = await ikb.select_create_advertisement_type(user[8]))
                
        return await call.answer(_messages['message'][user[8]]['error_show_alert_message_balance'].format(
            min_crypto_count_ad,
            call_message[1],
            min_currency_count_ad,
            user[7].upper(),
            balance_user,
            call_message[1]
        ), show_alert=True)

    await state.set_state(AdvertisementState.crypto.state)

    balance_user = await datapro.prosessing_select_one_balance_user(call.from_user.id, call_message[1])
    crypto_rate = 1

    async with state.proxy() as data:
        data['id_user'] = call.from_user.id
        data['type_add'] = call_message[2]
        data['crypto'] = call_message[1]


    await call.message.edit_text(_messages['message'][user[8]]['select_currency_ad_type_message'].format(
        _messages['message'][user[8]][f'select_cryptocurrency_ad_type_message_{call_message[2]}'],
        call_message[1]
    ), reply_markup = await ikb.select_create_advertisement_currency(user[8], call_message[2]))


@dp.callback_query_handler(Text(startswith='selectAdvertisementCurrency_'), state=AdvertisementState.crypto.state) # 4
async def advertisement_Currency_rate(call: types.CallbackQuery, state: FSMContext):
    call_message = call.data.split('_')

    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    count_payments = await datapro.processing_select_count_payments_user(call.from_user.id)

    if count_payments is None:
        await state.finish()
        return await call.message.edit_text(_messages['message'][user[8]]['error_payment_ad'].format(
            call_message[1].upper()
        ), reply_markup = await ikb.advertisement_add_payment(user[8]))


    await state.set_state(AdvertisementState.crypto_rates.state)

    async with state.proxy() as data:
        _type_add = data['type_add']
        data['currency'] = call_message[1].upper()
        _crypto = data['crypto']

    crypto_rates = _crypto + call_message[1].upper().replace("USD", "USDT") # call_message -> RUB or USD

    crypto_rate = 0

    if call_message[1] == "usd" and _crypto == "USDT":
        crypto_rate = 1

    if call_message[1] == "usd" and _crypto != "USDT" or call_message[1] == "rub" or call_message[1] != "usd" and _crypto == "USDT":
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)

    async with state.proxy() as data:
        data['crypto_rates'] = crypto_rate

    if call_message[1] == 'usd':
        crypto_rate = f'${crypto_rate}'
    if call_message[1] == 'rub':
        crypto_rate = f'{crypto_rate}₽'

    
    await call.message.edit_text(_messages['message'][user[8]]['select_currency_ad_rate_message'].format(
        call_message[1].upper(),
        _messages['message'][user[8]][f'select_cryptocurrency_ad_type_message_{_type_add}'],
        _crypto,
        crypto_rate,
        _crypto,
        crypto_rate
    ), reply_markup = await ikb.select_create_advertisement_currency_rate(user[8], 'title_fixed_select'))



@dp.callback_query_handler(text="crypto_rate_fixed", state=AdvertisementState.crypto_rates.state) # 4 | reset fixed cryptocurrency rate
async def advertisement_user_cryptocurrency_rate(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.crypto_rates.state)

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    async with state.proxy() as data:
        _type_add = data['type_add']
        call_message = data['currency']
        _crypto = data['crypto']

    crypto_rates = _crypto + call_message.replace("USD", "USDT") # call_message -> RUB or USD
    
    crypto_rate = ''

    call_message = call_message.lower()

    if call_message == "usd" and _crypto == "USDT":
        crypto_rate = 1

    if call_message == "usd" and _crypto != "USDT" or call_message == "rub" or call_message != "usd" and _crypto == "USDT":
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)
    
    async with state.proxy() as data:
        data['crypto_rates'] = crypto_rate

    if call_message == 'usd':
        crypto_rate = f'${crypto_rate}'
    if call_message == 'rub':
        crypto_rate = f'{crypto_rate}₽'

    try:
        await call.message.edit_text(_messages['message'][user[8]]['select_currency_ad_rate_message'].format(
            call_message.upper(),
            _messages['message'][user[8]][f'select_cryptocurrency_ad_type_message_{_type_add}'],
            _crypto,
            crypto_rate,
            _crypto,
            crypto_rate
        ), reply_markup = await ikb.select_create_advertisement_currency_rate(user[8], 'set_title_fixed_select'))
    except:
        pass

@dp.message_handler(state=AdvertisementState.crypto_rates.state) # 4
async def advertisement_user_cryptocurrency_rate_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        _type_add = data['type_add']
        call_message = data['currency']
        _crypto = data['crypto']

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
        data['crypto_rates'] = user_crypto_rate

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
    ), reply_markup = await ikb.select_create_advertisement_currency_rate(user[8], False))


@dp.callback_query_handler(text="continue", state=AdvertisementState.crypto_rates.state) # 5
async def advertisement_user_cryptocurrency_count(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.count.state)
    async with state.proxy() as data:
        _type_add = data['type_add']
        _crypto = data['crypto']

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    balance_user = await datapro.prosessing_select_one_balance_user(call.from_user.id, _crypto)

    currency_user_local_bot = user[7].upper() # RUB or USD

    crypto_rates = _crypto + currency_user_local_bot.replace("USD", "USDT")

    crypto_rate = 1
    if user[7] == "usd" and _crypto != "USDT" or user[7] == "rub" or user[7] != "usd" and _crypto == "USDT":
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)

    balance_rate = ""

    if _type_add == 'sell':
        if currency_user_local_bot == 'RUB':
            balance_rate = f'{(float(balance_user) * crypto_rate):.2f}₽'

        if currency_user_local_bot == 'USD':
            if _crypto != 'USDT':
                balance_rate = f'${(float(balance_user) * crypto_rate):.2f}'
            else:
                balance_rate = f'${balance_user}'        

    await call.message.edit_text(_messages['message'][user[8]][f'message_count_ad_crypto_{_type_add}'].format(
        _crypto,
        _messages['message'][user[8]][f'select_cryptocurrency_ad_type_message_{_type_add}'],
        balance_user,
        _crypto,
        balance_rate
    ), reply_markup = await ikb.advertisement_amount_user_max(user[8], balance_user, _crypto, _type=_type_add))


@dp.message_handler(state=AdvertisementState.count.state)
async def advertisement_amount_user_message(message: types.Message, state: FSMContext):
    user = await datapro.processing_select_all_info_user(message.from_user.id)
    
    async with state.proxy() as data:
        _type_add = data['type_add']
        _currency = data['currency'] 
        _crypto = data['crypto']

    balance_user = await datapro.prosessing_select_one_balance_user(message.from_user.id, _crypto)

    currency_user_local_bot = user[7].upper()

    crypto_rate = 1
    
    if user[7] == "usd" and _crypto != "USDT" or user[7] == "rub" or user[7] != "usd" and _crypto == "USDT":
        crypto_rates = _crypto+currency_user_local_bot.replace('USD', 'USDT')
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)

    min_crypto_count_ad, min_currency_count_ad = await amount_balance_min_and_max(_crypto, user[7], crypto_rate)

    try:
        message_amount = float(message.text)

        if _type_add == 'sell':
            if message_amount > balance_user:
                return await message.answer(_messages['message'][user[8]]['error_message_total_balance_max'].format(balance_user, _crypto))

            if message_amount < min_crypto_count_ad:                
                return await message.answer(_messages['message'][user[8]]['error_message_total_balance_min'].format(min_crypto_count_ad, _crypto, min_currency_count_ad))
        
        crypto_limits = await datapro.processing_select_limitations_crypto(_crypto)

        if _type_add == 'buy':
            if message_amount > crypto_limits[0]:
                return await message.answer(_messages['message'][user[8]]['error_message_total_buy_max'].format(crypto_limits[0], _crypto))
            if message_amount < crypto_limits[1]:
                return await message.answer(_messages['message'][user[8]]['error_message_total_buy_min'].format(crypto_limits[1], _crypto))

    except Exception:
        return await message.answer(_messages['message'][user[8]]['error_ad_crypto_rate'])

    async with state.proxy() as data:
        data['count'] = message_amount

    await state.set_state(AdvertisementState.limit_deals.state)

    min_limit = None
    max_limit = None

    if _currency == 'RUB':
        max_limit = 5_000_000
        min_limit = 100
        message_amount_currency = str(crypto_rate*message_amount) + '₽'
        _amount_currency = crypto_rate * float(message_amount)

    if _currency == 'USD':
        max_limit = 100_000
        min_limit = 2
        message_amount_currency = '$' + str(crypto_rate*message_amount)
        _amount_currency = crypto_rate * float(message_amount)
        if _crypto == 'USDT':
            message_amount_currency = '$' + str(message_amount)

    await message.answer(_messages['message'][user[8]]['message_limit_ad_orders'].format(
        _currency,
        min_limit,
        message_amount_currency,
        min_limit,
        max_limit,
        message_amount,
        _crypto,
        message_amount_currency,
        min_limit,
        _currency,
        max_limit,
        _currency
    ), reply_markup = await ikb.advertisement_limit(user[8], min_limit, _amount_currency, max_limit))


@dp.callback_query_handler(text="sellAmountAdvertisement_max", state=AdvertisementState.count.state)
async def advertisement_amount_user(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.limit_deals.state)
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    async with state.proxy() as data:
        _currency = data['currency']
        _crypto = data['crypto']

    crypto_rate = 1
    if _currency == "USD" and _crypto != "USDT" or _currency == "RUB" or _currency != "USD" and _crypto == "USDT":
        crypto_rates = _crypto + _currency.replace('USD', 'USDT')
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)

    message_amount =  await datapro.prosessing_select_one_balance_user(call.from_user.id, _crypto)

    min_limit, max_limit, message_amount_currency, _amount_currency = await limits(_currency, _crypto, crypto_rate, message_amount)

    async with state.proxy() as data:
        data['count'] = message_amount

    await call.message.edit_text(_messages['message'][user[8]]['message_limit_ad_orders'].format(
        _currency,
        min_limit,
        message_amount_currency,
        min_limit,
        max_limit,
        message_amount,
        _crypto,
        message_amount_currency,
        min_limit,
        _currency,
        max_limit,
        _currency
    ), reply_markup = await ikb.advertisement_limit(user[8], min_limit, _amount_currency, max_limit))


@dp.message_handler(state=AdvertisementState.limit_deals.state)
async def advertisement_limit_orders(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        _currency = data['currency']
        _crypto = data['crypto']

    user = await datapro.processing_select_all_info_user(message.from_user.id)

    crypto_rate = 1
    if user[7] == "usd" and _crypto != "USDT" or user[7] == "rub" or user[7] != "usd" and _crypto == "USDT":
        crypto_rates = _crypto + user[7].upper().replace('USD', 'USDT')
        crypto_rate = await datapro.processing_select_one_crypto_rates(crypto_rates)
    
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
    
    async with state.proxy() as data:
        data['limit_deals'] = [float(user_limit[0]), float(user_limit[1])]

    await state.set_state(AdvertisementState.payment_method.state)

    await message.answer(_messages['message'][user[8]]['select_payments_method_sell'],
                                 reply_markup = await ikb.select_advertisement_payment(user[8], datapro, message.from_user.id, 'none', _currency))


@dp.callback_query_handler(Text(startswith='advertisementLimit_'), state=AdvertisementState.limit_deals.state)
async def advertisement_limits(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.payment_method.state)
    user_limit = call.data.split('_')
    
    async with state.proxy() as data:
        data['limit_deals'] = [float(user_limit[1]), float(user_limit[2])] # добавляем лимиты в виде списка [min, max]
        currency = data['currency']

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['select_payments_method_sell'],
                                 reply_markup = await ikb.select_advertisement_payment(user[8], datapro, call.from_user.id, 'none', currency))



@dp.callback_query_handler(Text(startswith='advertisementPayment_'), state=AdvertisementState.payment_method.state)
async def select_payments_new(call: types.CallbackQuery, state: FSMContext):
    payment_id = call.data.split('_')[1]

    async with state.proxy() as data:
        _payment_method = data.get('payment_method', [])  # Получаем текущий список способов оплаты
    
        if payment_id in _payment_method:
            _payment_method.remove(payment_id) # Удаляем способ оплаты
    
        elif not payment_id in _payment_method:
            _payment_method.append(payment_id)  # Добавляем новый способ оплаты
    
        await state.update_data(payment_method=_payment_method)  # Обновляем состояние с новым списком способов оплаты
    
    async with state.proxy() as data:
        _payment_methods = data['payment_method']  # Получаем обновленный список способов оплаты
        currency = data['currency']

    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    try:
        await call.message.edit_text(_messages['message'][user[8]]['select_payments_method_sell'],
                                    reply_markup = await ikb.select_advertisement_payment(user[8], datapro, call.from_user.id, _payment_methods, currency))
    except exceptions.MessageNotModified:
        pass



@dp.callback_query_handler(text='continue_advertisement', state=AdvertisementState.payment_method.state)
async def call_continue_advertisement(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.amount_time.state)

    async with state.proxy() as data:
        data['amount_time'] = 15

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    try:
        await call.message.edit_text(_messages['message'][user[8]]['select_time_deals'],
                                    reply_markup = await ikb.select_timer_deals(user[8], 'timerDeals_15'))
    except exceptions.MessageNotModified:
        pass


@dp.callback_query_handler(Text(startswith='timerDeals_'), state=AdvertisementState.amount_time.state)
async def call_continue_advertisement(call: types.CallbackQuery, state: FSMContext):
    _timer = call.data.split('_')[1]

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    async with state.proxy() as data:
        data['amount_time'] = int(_timer)

    try:
        await call.message.edit_text(_messages['message'][user[8]]['select_time_deals'],
                                    reply_markup = await ikb.select_timer_deals(user[8], call.data))
    except exceptions.MessageNotModified:
        pass


@dp.callback_query_handler(text='continue_timer_deals', state=AdvertisementState.amount_time.state)
async def call_verification_and_confirmation(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.date.state)
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    async with state.proxy() as data:
        _type = data['type_add']
        crypto = data['crypto']
        currency = data['currency']
        crypto_rates = data['crypto_rates']
        count = data['count']
        limit_deals = data['limit_deals'] # list deals limit
        payment_method = data['payment_method']
        amount_time = data['amount_time']
        data['date'] = datetime.now().date()
        data['advertisement'] = False
        data['status'] = False

    _payment_method = ""
    

    for number, payment in enumerate(payment_method):
        pay = await datapro.processing_select_payment_info(call.from_user.id, int(payment))
        account_number = ''
        if account_number:
            account_number = '*' + pay[0][-4:]
        _payment_method += f'{number+1}) {pay[3]} {account_number}\n'

    _amount_time = ""

    if amount_time == 15 or amount_time == 30:
        _amount_time = _messages['button'][user[8]]['time_min'].format(amount_time)

    if amount_time == 1:
        _amount_time = _messages['button'][user[8]]['time_hour'].format(amount_time)

    _type_add = _messages['button'][user[8]][_type]

    await call.message.edit_text(_messages['message'][user[8]]['verification_and_confirmation'].format(
        _type_add,
        crypto,
        currency,
        crypto_rates,
        currency,
        count,
        crypto,
        limit_deals[0],
        currency,
        float(limit_deals[1]),
        currency,
        _payment_method,
        _amount_time
    ), reply_markup = await ikb.create_offer_user(user[8]))


@dp.callback_query_handler(text='create_p2p_offer_user', state=AdvertisementState.date.state)
async def call_create_offer(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdvertisementState.advertisement.state)
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    async with state.proxy() as data:
        crypto = data['crypto']
        type_add = data['type_add']
        currency = data['currency']
        crypto_rates = data['crypto_rates']
        count = data['count']
        limit_deals = data['limit_deals'] # list deals limit
        payment_method = data['payment_method']
        amount_time = data['amount_time']
        date = data['date']
        advertisement = data['advertisement']
        status = data['status']

    payment_method = ','.join(payment_method)

    await datapro.processing_add_advertisement(crypto,
                                               currency,
                                               crypto_rates,
                                               count,
                                               payment_method,
                                               amount_time,
                                               date,
                                               advertisement,
                                               status,
                                               call.from_user.id,
                                               type_add,
                                               limit_deals)
    # await datapro.processing_minus_crypto_balance(call.from_user.id, crypto, count)
    
    await state.finish()
    await call.answer(_messages['message'][user[8]]['alert_success_create_offer'], show_alert=False)
    await call.message.edit_text(_messages['message'][user[8]]['select_type_ad'],
                                 reply_markup = await ikb.select_create_advertisement_type(user[8]))


@dp.callback_query_handler(text='Advertisement_cancel', state=AdvertisementState)
async def call_cancel_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.reset_state(with_data=False)

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['select_type_ad'],
                                 reply_markup = await ikb.select_create_advertisement_type(user[8]))