from aiogram import types

from loader import dp

from src.system.message_system import _messages
from src.processing import data_processing as datapro
from src.handlers.keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text="wallet")
async def call_wallet(call: types.CallbackQuery):
    user = await datapro.processing_select_all_info_user(call.from_user.id)
    
    crypto_currency = await datapro.processing_select_all_currency()
    balances = await datapro.processing_select_crypto_balances(call.from_user.id)

    rows = ""

    if balances is None:
        return await call.message.edit_text(_messages['message'][user[8]]['wallet'].format(_messages['message'][user[8]]['none_balances']),
                                            reply_markup=await ikb.selection_wallet(user[8]))

    usdt_balance = None

    for balance in balances:
        currency = user[7].upper()
        for crypto in crypto_currency:
            
            if balance[0] in crypto[0]:
                if currency == 'RUB':
                    if currency == 'RUB' and currency in crypto[0][len(crypto[0])//2:]:
                        rows += f"· <b>{balance[0]}:</b> {balance[1]:.8f} ({float(balance[1])*crypto[1]:.2f}₽)\n\n"
                
                if currency == 'USD':
                    if balance[0] == "USDT":
                        usdt_balance = balance
                        continue

                    if currency == 'USD' and currency in crypto[0][len(crypto[0])//2:]:
                        rows += f"· <b>{balance[0]}:</b> {balance[1]:.8f} (${float(balance[1])*crypto[1]:.2f})\n\n"




    if usdt_balance:
        rows += f"· <b>{usdt_balance[0]}:</b> {usdt_balance[1]:.8f} (${float(usdt_balance[1]):.2f})\n\n"

    await call.message.edit_text(_messages['message'][user[8]]['wallet'].format(rows),
                                 reply_markup=await ikb.selection_wallet(user[8]))
