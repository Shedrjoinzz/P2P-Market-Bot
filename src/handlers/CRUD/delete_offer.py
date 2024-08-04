from aiogram import types
from aiogram.dispatcher.filters import Text

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb
from src.handlers.user.offers import offer as main_offer


@dp.callback_query_handler(Text(startswith='offerDelete_'))
async def offer_delete(call: types.CallbackQuery):
    call_msg = call.data.split('_')

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['delete_offer'],
                                 reply_markup = await ikb.delete_offer(user[8], int(call_msg[1]), int(call_msg[2])))


@dp.callback_query_handler(Text(startswith='offerDeleteYes_'))
async def offer_delete_yes(call: types.CallbackQuery):
    call_msg = call.data.split('_')

    offer = await datapro.processing_select_offer(int(call_msg[1]))
    
    await datapro.processing_minus_crypto_balance(call.from_user.id, offer[1], offer[4], method=False)

    await datapro.processing_delete_offer(call.from_user.id, int(call_msg[1]))

    user = await datapro.processing_select_all_info_user(call.from_user.id)

    await call.answer(_messages['message'][user[8]]['success_delete_offer'])

    await call.message.edit_text(_messages['message'][user[8]]['offers_manager'],
                                 reply_markup = await ikb.offers(user[8], datapro, call.from_user.id, int(call_msg[2])))


@dp.callback_query_handler(Text(startswith='offerDeleteNo_'))
async def offer_delete_no(call: types.CallbackQuery):
    await main_offer(call)