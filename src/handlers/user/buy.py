from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from src.handlers.keyboards import inline_keyboards as ikb
from src.system.message_system import _messages
from src.processing import data_processing as datapro

@dp.callback_query_handler(text='buy')
async def sell_crypto(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    await call.message.edit_text(_messages['message'][user[8]]['select_cryptocurrency_buy'],
                              reply_markup = await ikb.market_sell(user[8], datapro, call.from_user.id))

