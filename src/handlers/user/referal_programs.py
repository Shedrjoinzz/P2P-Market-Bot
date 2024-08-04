from aiogram import types

from src.system.message_system import _messages
from loader import dp
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text="referral_program")
async def information_referal_program(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    referrals = await datapro.processing_select_all_referrals(call.from_user.id)

    await call.message.edit_text(_messages['message'][user[8]]['referrals_information'].format(id_user=call.from_user.id, referrals=referrals),
                                 reply_markup = await ikb.back_to_setting(user[8]))

