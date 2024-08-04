from aiogram import types
from aiogram.dispatcher.filters import Text

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(Text(startswith='page:'))
async def call_page_my_offers(call: types.CallbackQuery):
    page = int(call.data.split(':')[1])
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    await call.message.edit_text(_messages['message'][user[8]]['offers_manager'],
                                 reply_markup = await ikb.offers(user[8], datapro, call.from_user.id, page))