from aiogram import types

from datetime import datetime

from loader import dp, bot
from src.handlers.keyboards import inline_keyboards as ikb
from src.system.message_system import _messages
from src.system.ban_system import is_ban_user
from src.processing import data_processing as datapro


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    is_user_ban = await is_ban_user(message.chat.id)

    start_message = message.text
    ref_id = str(start_message[7:])
    list_start_message = start_message[7:].split('-')

    user = await datapro.processing_select_all_info_user(message.chat.id)
    if is_user_ban == True and user != None:
        info_ban = await datapro.processing_select_info_ban_user(message.chat.id)
        await message.answer(_messages['message'][user[8]]['ban'])
        return await message.answer(f'<b>Description ban:</b>\n<i>-{info_ban[1]}</i>')
    
    if user == None:
        code_lang = message.from_user.language_code
        ref_id = list_start_message[0]
        currency = 'rub'

        if code_lang != 'ru' and code_lang != 'en':
            code_lang = 'en'
            currency = 'usd'

        await datapro.processing_insert_new_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, f'@{message.from_user.username}', 0, 0, datetime.now().date(), code_lang, currency)

        if ref_id != '':
            if ref_id != str(message.chat.id):
                try: # блок исключений для проверки идентификатора пользователя на тип int
                    is_ref_user = await datapro.processing_select_all_info_user(int(ref_id)) # проверка есть ли такой пользователь в базе

                    if is_ref_user != None: # если пользователь есть то вернёт данные (data != None)
                        await datapro.processing_insert_new_ref(message.from_user.id, int(ref_id), datetime.now().date()) # если рефовод есть, записываем данные в таблицу реф-системы и добавляем в качестве рефовода ref_id с типом int
                        try: # вдруг рефовод заблокировал бота
                            await bot.send_message(int(ref_id), _messages['message'][code_lang]['new_ref']) # так-же сообщение рефоводу что по его ссылке перешёл новый пользователь
                        except:
                            pass
                    else:
                        await datapro.processing_insert_new_ref(message.from_user.id, None, datetime.now().date()) # иначе если такого рефовода нет в базе то записываем ref_id как None

                except ValueError: # иначе будет такая запись в бд реф-системы
                    await datapro.processing_insert_new_ref(message.from_user.id, None, datetime.now().date())

        if ref_id == '':
            await datapro.processing_insert_new_ref(message.from_user.id, None, datetime.now().date())
                    
        if 'market' in list_start_message: # если в ссылке содержалось слово market то откроется раздел P2P (заметим что этот блок для тех кто ещё не зарегестрирован в боте, по этому берём code_lang, а не user[8] -> 'ru' or 'en')
            return await message.answer(_messages['message'][code_lang]['p2p'],
                                reply_markup = await ikb.market_menu(lang_code=code_lang, datapro=datapro, id_user=message.from_user.id))

        return await message.answer(_messages['message'][code_lang]['new_user'], reply_markup= await ikb.main_menu(lang_code=code_lang))


    if "market" in list_start_message:
        return await message.answer(_messages['message'][user[8]]['p2p'],
                                reply_markup = await ikb.market_menu(lang_code=user[8], datapro=datapro, id_user=message.from_user.id))

    await dp.storage.reset_state(chat=message.chat.id, user=message.from_user.id)
    print('c,hjc')
    await message.answer(_messages['message'][user[8]]['old_user'], # если пользователь есть то отправить стартовое сообщение old-пользователю
                         reply_markup= await ikb.main_menu(lang_code=user[8]))