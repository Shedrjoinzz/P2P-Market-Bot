from aiogram import types

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text="market")
async def market_p2p(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)

    user_market = await datapro.processing_select_user_p2p_market(call.from_user.id)

    if user_market is None:
        await datapro.processing_add_user_p2p_market(call.from_user.id, True, user[7].upper())

    await call.message.edit_text(_messages['message'][user[8]]['p2p'],
                                 reply_markup = await ikb.market_menu(lang_code=user[8], datapro=datapro, id_user=call.from_user.id))
