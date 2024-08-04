from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram import exceptions

from loader import dp
from src.handlers.keyboards import inline_keyboards as ikb
from src.system.message_system import _messages
from src.processing import data_processing as datapro
from src.states.state import Payments, AdvertisementState

import asyncio



@dp.callback_query_handler(text='add_payment_method')
async def call_add_payment_method(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    count_payments = await datapro.processing_select_count_payments_user(call.from_user.id)

    limit_payments = 15
    if not count_payments is None:
        if count_payments > limit_payments:
            return await call.answer(_messages['message'][user[8]]['error_max_count_payments'].format(limit_payments), show_alert=True)

    await call.message.edit_text(_messages['message'][user[8]]['message_select_p2p_payments_currency'],
                                 reply_markup = await ikb.select_currency_bot(user[8], user[7], 'Payments', 'payment_currency'))


@dp.callback_query_handler(Text(startswith='selectCurrencyPayments_'))
async def add_payments_user(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Payments.currency.state)

    currency = call.data.split('_')[1].upper()

    async with state.proxy() as data:
        data['currency'] = currency

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['message_select_payments'].format(currency),
                                 reply_markup=await ikb.select_payments_admin(user[8], currency, datapro))


@dp.callback_query_handler(Text(startswith='addPaymentsAdmin_'), state=Payments.currency.state)
async def add_payments_users(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Payments.payment.state)
    payments = call.data.split('_')

    async with state.proxy() as data:
        data['payment'] = payments[1]
        data['_type'] = payments[2]

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['message_payments_data'].format(payments[1]),
                                 reply_markup = await ikb.state_add_payments_back(user[8]))


@dp.message_handler(state=Payments.payment.state)
async def message_data_payments(message: types.Message, state: FSMContext):
    payment_data = message.text
    user = await datapro.processing_select_all_info_user(message.from_user.id)

    if len(payment_data) < 5:
        return await message.answer(_messages['message'][user[8]]['message_min_characters'])
    
    if len(payment_data) > 150:
        return await message.answer(_messages['message'][user[8]]['message_max_characters'])
    
    async with state.proxy() as data:
        data['data'] = message.text

    await state.set_state(Payments.title.state)

    await message.answer(_messages['message'][user[8]]['message_add_title_payments'],
                                 reply_markup = await ikb.skip_add_title_payments(user[8]))



@dp.callback_query_handler(text='skip', state=Payments.title.state)
async def call_skip_add_title_payments(call: types.CallbackQuery, state: FSMContext):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    async with state.proxy() as data:
        await datapro.processing_add_payments_user(call.from_user.id,
                                                   data['payment'],
                                                   data['_type'],
                                                   data['data'],
                                                   None,
                                                   data['currency'])    
    await state.finish()
    
    await call.message.edit_text(_messages['message'][user[8]]['message_successfully_add_payments'])
    
    await call.message.answer(_messages['message'][user[8]]['p2p_payment'],
                                 reply_markup = await ikb.select_all_payment_user(user[8], datapro, call.from_user.id))


@dp.message_handler(state=Payments.title.state)
async def message_title_payments(message: types.Message, state: FSMContext):
    payment_data = message.text

    user = await datapro.processing_select_all_info_user(message.from_user.id)

    if len(payment_data) > 20:
        payment_data = payment_data[:20]

    async with state.proxy() as data:
        await datapro.processing_add_payments_user(message.from_user.id,
                                                   data['payment'],
                                                   data['_type'],
                                                   data['data'],
                                                   payment_data,
                                                   data['currency'])    
    await state.finish()
    await message.answer(_messages['message'][user[8]]['message_successfully_add_payments'])
    await message.answer(_messages['message'][user[8]]['p2p_payment'],
                                 reply_markup = await ikb.select_all_payment_user(user[8], datapro, message.from_user.id))


@dp.callback_query_handler(text='add_payment_method_state', state=AdvertisementState)
async def call_add_payment_method_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    count_payments = await datapro.processing_select_count_payments_user(call.from_user.id)

    limit_payments = 15
    if not count_payments is None:
        if count_payments > limit_payments:
            return await call.answer(_messages['message'][user[8]]['error_max_count_payments'].format(limit_payments), show_alert=True)

    await call.message.edit_text(_messages['message'][user[8]]['message_select_p2p_payments_currency'],
                                reply_markup = await ikb.select_currency_bot(user[8], user[7], 'Payments', 'payment_currency'))


@dp.callback_query_handler(text='cancel_add_payment_method', state=Payments)
async def cal_cancel_add_payment_method(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['message_select_p2p_payments_currency'],
                                reply_markup = await ikb.select_currency_bot(user[8], user[7], 'Payments', 'payment_currency'))

