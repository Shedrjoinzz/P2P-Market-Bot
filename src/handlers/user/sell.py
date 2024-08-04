from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from src.handlers.keyboards import inline_keyboards as ikb
from src.system.message_system import _messages
from src.processing import data_processing as datapro


@dp.callback_query_handler(text='sell')
async def sell_crypto(call: types.CallbackQuery):
    print(1)
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    await call.message.edit_text(_messages['message'][user[8]]['select_cryptocurrency_sell'],
                              reply_markup = await ikb.market_sell(user[8], datapro, call.from_user.id))


@dp.callback_query_handler(Text(startswith='p2pSellType_'))
async def sell_pay(call: types.CallbackQuery):
    # print(call.data)
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    await dp.skip_updates()
    p2p_currency = await datapro.processing_select_user_p2p_market(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['select_payment_sell'].format(p2p_currency[1]),
                              reply_markup = await ikb.select_sell_payment_method_type(user[8], p2p_currency[1], datapro, call.data.split('_')[1]))
    

@dp.callback_query_handler(Text(startswith='p2pTypePayments_'))
async def give_offers_users(call: types.CallbackQuery):
    call_data = call.data.split('_')
    # print('call_data', call_data)
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    user_p2p_market = await datapro.processing_select_user_p2p_market(call.from_user.id)
    
    sell_offers = await datapro.processing_select_advertisement_user_method(call_data[1], user_p2p_market[1], str(call_data[2]), "buy")

    print('sell_offers', sell_offers)