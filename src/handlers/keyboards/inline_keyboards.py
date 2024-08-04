from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.filters.filter import filter_decimal, one_crypto_rate
from src.system.message_system import _messages


async def main_menu(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['wallet'], callback_data='wallet')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p'], callback_data='market')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['setting'], callback_data='setting')
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup

# i[0].advertisement - это статус объявление (снят - публикован -> False - True)
# i[0].status - это включение торгов (выключены - включены -> False - True)
async def market_menu(lang_code, datapro, id_user):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_buy'], callback_data="buy")
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_sell'], callback_data="sell")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_order'], callback_data="order_history")

    select_ad = await datapro.processing_select_advertisement(id_user)
    _count = 0
    _activate = 0

    if select_ad:
        for i in select_ad:
            if i[0].advertisement == True and i[0].status == True:
                _activate += 1
            _count += 1

    my_offers = InlineKeyboardButton(text=_messages['button'][lang_code]['advertisement_market'].format(_activate, _count), callback_data='myOffersPage_1')
    in4 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_offer'], callback_data="create_offer")
    in5 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_payment'], callback_data="payment_currency")
    in6 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_profile'], callback_data="p2p_profile")
    in7 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="back_menu")
    inline_markup.add(in1, in2)
    inline_markup.add(in3)

    if _count:
        inline_markup.add(my_offers)
    
    if _count == 0:
        inline_markup.add(in4)
    
    inline_markup.add(in5)
    inline_markup.add(in6)
    inline_markup.add(in7)
    return inline_markup


async def market_payment_currency(lang_code, currency_market):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['currency_p2p_market'].format(currency_market), callback_data="currency_market")
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['method_payment'], callback_data="payment_method")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data='market')
    inline_markup.add(in1)
    inline_markup.add(in2)
    inline_markup.add(in3)
    return inline_markup



async def crypto_deposit(lang_code, datapro):
    inline_markup = InlineKeyboardMarkup()
    for cryptocurrency in await datapro.processing_select_listing_crypto():
        in1 = InlineKeyboardButton(text=str(cryptocurrency), callback_data=f"deposit_{cryptocurrency}")
        inline_markup.add(in1)
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="back_menu")
    inline_markup.add(in2)
    return inline_markup


async def selection_wallet(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['deposit'], callback_data='deposit')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['withdraw'], callback_data='withdraw')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="back_menu")
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup


async def selection_network(lang_code, network: list):
    inline_markup = InlineKeyboardMarkup()
    for net in network:
        in1 = InlineKeyboardButton(text=net, callback_data=f"network_{net}")
        inline_markup.add(in1)
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="deposit_")
    inline_markup.add(in2)
    return inline_markup


async def back_to_menu(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="deposit")
    inline_markup.add(in1)
    return inline_markup


async def setting_menu(lang_code, currencu):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['referral_program'], callback_data="referral_program")
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['bot_language'], callback_data="bot_language")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['currency_bot'].format(currencu), callback_data="currency_bot")
    in4 = InlineKeyboardButton(text=_messages['button'][lang_code]['contac_us'], url="t.me/Vagif0")
    in5 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="back_menu")
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    inline_markup.add(in4)
    inline_markup.add(in5)
    return inline_markup


async def back_to_setting(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="setting")
    inline_markup.add(in1)
    return inline_markup
    

async def select_language_bot(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text="🇺🇸 English", callback_data="selectLanguageBot_en")
    in2 = InlineKeyboardButton(text="🇷🇺 Русский", callback_data="selectLanguageBot_ru")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="setting")
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup


async def select_currency_bot(lang_code, currency, _local, _call):
    rub = "RUB"
    usd = "USD"

    if currency.upper() == rub:
       rub = "• RUB •" 
    if currency.upper() == usd:
       usd = "• USD •"

    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=rub, callback_data=f"selectCurrency{_local}_rub")
    in2 = InlineKeyboardButton(text=usd, callback_data=f"selectCurrency{_local}_usd")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=_call)
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup


async def select_create_advertisement_type(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_buy'], callback_data="createAdvertisement_buy")
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_sell'], callback_data="createAdvertisement_sell")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="market")
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup


async def select_create_advertisement_cryptocurrency(lang_code, datapro, _type):
    inline_markup = InlineKeyboardMarkup(row_width=4)
    crypto_listing = await datapro.processing_select_listing_crypto()
    for cryptocurrency in crypto_listing:
        in1 = InlineKeyboardButton(text=str(cryptocurrency), callback_data=f"selectAdvertisementCryptocurrency_{cryptocurrency}_{_type}")
        inline_markup.add(in1)
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")
    inline_markup.add(in2)
    return inline_markup


async def select_create_advertisement_currency(lang_code, _type):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text="RUB", callback_data="selectAdvertisementCurrency_rub")
    in2 = InlineKeyboardButton(text="USD", callback_data="selectAdvertisementCurrency_usd")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup


async def select_create_advertisement_currency_rate(lang_code, select_fixed):
    title_fixed_select = _messages['button'][lang_code]['currency_ad_rate']
    if select_fixed:
        title_fixed_select = f"• {_messages['button'][lang_code]['currency_ad_rate']} •"

    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=title_fixed_select, callback_data="crypto_rate_fixed")
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['continue'], callback_data="continue")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")
    inline_markup.add(in1)
    inline_markup.add(in2)
    inline_markup.add(in3)
    return inline_markup


async def advertisement_amount_user_max(lang_code, amount, crypto, _type='sell'):
    inline_matkup = InlineKeyboardMarkup()
    
    
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['message_max_amount_ad_user'].format(amount, crypto), callback_data=f"{_type}AmountAdvertisement_max")
    if _type == 'sell':
        inline_matkup.add(in1)
    
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")
    inline_matkup.add(in2)
    return inline_matkup


async def advertisement_limit(lang_code, min_limit, user_limit, max_limit):
    inline_keyboard = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=f'{min_limit}-{user_limit:.2f}', callback_data=f'advertisementLimit_{min_limit}_{user_limit}')
    in2 = InlineKeyboardButton(text=f'{min_limit}-{max_limit}', callback_data=f'advertisementLimit_{min_limit}_{max_limit}')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")
    inline_keyboard.add(in1)
    inline_keyboard.add(in2)
    inline_keyboard.add(in3)
    return inline_keyboard


async def advertisement_add_payment(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['add_new_payment'], callback_data='payment_method')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="create_offer")
    inline_markup.add(in1)
    inline_markup.add(in2)
    return inline_markup


async def select_payments_admin(lang_code, currency, datapro):
    inline_markup = InlineKeyboardMarkup()    
    payments = await datapro.processing_select_payments()
    for payment in payments:
        pay = ''
        _type = ''
        
        if lang_code == 'ru':
            pay = payment[0].name.split('_')[1]
            _type = payment[0].type.split('_')[1]

        if lang_code == 'en':
            pay = payment[0].name.split('_')[0]
            _type = payment[0].type.split('_')[0]

        if lang_code != 'ru' and lang_code != 'en':
            pay = payment[0].name.split('_')[0]
            _type = payment[0].type.split('_')[0]

        if currency in payment[0].currency:
            in1 = InlineKeyboardButton(text=f'{pay}', callback_data=f'addPaymentsAdmin_{pay}_{_type}')
            inline_markup.add(in1)

    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="cancel_add_payment_method")
    inline_markup.add(in2)
    return inline_markup



async def select_all_payment_user(lang_code, datapro, id_user):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['add_new_payment'], callback_data='add_payment_method')
    inline_markup.add(in1)

    numeb = await datapro.processing_select_payments_method(id_user, _all=False)

    for i in numeb:
        account_number = '*' + i[0].payment_data[-4:]
        if not i[0].payment_title is None:
            account_number = '• ' + i[0].payment_title

        in2 = InlineKeyboardButton(text=f'{i[0].payment_method} {account_number}', callback_data=f'givePayment_{i[0].id}')
        inline_markup.add(in2)
    
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data="payment_currency")
    inline_markup.add(in3)
    return inline_markup


async def state_add_payments_back(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data='cancel_add_payment_method')
    inline_markup.add(in1)
    return inline_markup


async def skip_add_title_payments(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['skip'], callback_data='skip')
    inline_markup.add(in1)
    return inline_markup


async def menu_payment_nav(lang_code, _id):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['edit_title_payment'], callback_data=f'editPayment_{_id}')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['delete_payment'], callback_data=f'deletePayment_{_id}')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f'payment_method')
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup


async def cancel_edit_payment(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data='cancel_edit_payment')
    inline_markup.add(in1)
    return inline_markup


async def is_delete_payment(lang_code, _id):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['yes'], callback_data=f'yesDelete_{_id}')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['no'], callback_data=f'givePayment_{_id}')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f'givePayment_{_id}')
    inline_markup.add(in1, in2)
    inline_markup.add(in3)
    return inline_markup


async def select_advertisement_payment(lang_code, datapro, id_user, payment_id, currency):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['add_new_payment'], callback_data='add_payment_method_state')
    inline_markup.add(in1)

    numeb = await datapro.processing_select_payments_method(id_user, _all=False)

    for i in numeb:
        if i[0].payment_currency == currency:
            account_number = '*' + i[0].payment_data[-4:]
            if not i[0].payment_title is None:
                account_number = '- ' + i[0].payment_title

            in2 = InlineKeyboardButton(text=f'{i[0].payment_method} {account_number}', callback_data=f'advertisementPayment_{i[0].id}')
            for pay_id in payment_id:
                if in2.callback_data == f'advertisementPayment_{pay_id}':
                    in2.text = f'• {in2.text} •'
                else:
                    in2.text = f'{in2.text}'

            inline_markup.add(in2)
    
    if payment_id != [] and payment_id != 'none':
        in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['continue'], callback_data="continue_advertisement")
        inline_markup.add(in3)
    
    in4 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")
    inline_markup.add(in4)
    return inline_markup


async def select_timer_deals(lang_code, _timer):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['time_min'].format('15'), callback_data='timerDeals_15')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['time_min'].format('30'), callback_data='timerDeals_30')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['time_hour'].format('1'), callback_data='timerDeals_1')
    in4 = InlineKeyboardButton(text=_messages['button'][lang_code]['continue'], callback_data='continue_timer_deals')
    in5 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")

    if _timer == in1.callback_data:
        in1.text = f'• {in1.text} •'

    if _timer == in2.callback_data:
        in2.text = f'• {in2.text} •' 

    if _timer == in3.callback_data:
        in3.text = f'• {in3.text} •' 

    inline_markup.add(in1, in2, in3)
    inline_markup.add(in4)
    inline_markup.add(in5)
    return inline_markup


async def create_offer_user(lang_code):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_offer'], callback_data='create_p2p_offer_user')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['cancel_state'], callback_data="Advertisement_cancel")
    inline_markup.add(in1)
    inline_markup.add(in2)
    return inline_markup


async def market_sell(lang_code, datapro, id_user):
    inline_markup = InlineKeyboardMarkup(row_width=4)

    user_p2p_currency = await datapro.processing_select_user_p2p_market(id_user)

    crypto_listing = await datapro.processing_select_listing_crypto()

    if user_p2p_currency:
        for cryptocurrency in crypto_listing:
            user_max_rates_sell = await datapro.processing_select_count_create_type_crypto_advertisement(cryptocurrency)
            crypto_rate = await one_crypto_rate(cryptocurrency, user_p2p_currency[1], datapro)
            crypto_rate_and_currency_char = f"{crypto_rate}"

            if user_p2p_currency[1] == 'USD':
                crypto_rate_and_currency_char = f"${crypto_rate_and_currency_char}"

            if user_p2p_currency[1] == 'RUB':
                crypto_rate_and_currency_char = f"{crypto_rate_and_currency_char}₽"

            if user_max_rates_sell is None:
                user_max_rates_sell = 0

            in1 = InlineKeyboardButton(text=f'{cryptocurrency} • {crypto_rate_and_currency_char} • {user_max_rates_sell}', callback_data=f'p2pSellType_{cryptocurrency}')
            inline_markup.add(in1)

    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data='market')
    inline_markup.add(in3)
    return inline_markup


async def offers(lang_code, datapro, id_user, page_id):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['p2p_offer'], callback_data='create_offer')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['active_trades'], callback_data='resume_trades')
    inline_markup.add(in1)
    inline_markup.add(in2)

    select_advertisement = await datapro.processing_select_advertisement(id_user)

    page = page_id
    per_page = 5
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    crypto_rates = ''

    if select_advertisement:
        current_page_items = select_advertisement[start_index:end_index]

        for advertisement_m in current_page_items:
            for advertisement in advertisement_m:

                if advertisement.currency == 'USD':
                    crypto_rates = f'${advertisement.crypto_rates}'

                if advertisement.currency == 'RUB':
                    crypto_rates = f'{advertisement.crypto_rates}₽'
                volume = await filter_decimal(advertisement.count)

                symbol_status_offer = '🔘'
                
                if advertisement.advertisement:
                    symbol_status_offer = '🟢'

                in3 = InlineKeyboardButton(text=f"{symbol_status_offer} {_messages['button'][lang_code][advertisement.type_add]} • {volume} • {advertisement.crypto} • {crypto_rates}", callback_data=f'openOfferEdit_{advertisement.id}_{page}')
                inline_markup.add(in3)

        if page > 1:
            prev_button = InlineKeyboardButton(text=f'⬅️', callback_data=f'page:{page-1}')
            inline_markup.add(prev_button)
            
        if end_index < len(select_advertisement):
            next_button = InlineKeyboardButton(text=f'➡️', callback_data=f'page:{page+1}')
            inline_markup.add(next_button)

    in5 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data='market')
    inline_markup.add(in5)
    return inline_markup
    

async def view_offer(lang_code, status_offer, id_offer, page):
    inline_markup = InlineKeyboardMarkup(row_width=2)

    json_key_turn_offer_status = 'turn_offer_off'

    if status_offer:
        json_key_turn_offer_status = 'turn_offer_on'

    in1 = InlineKeyboardButton(text=_messages['button'][lang_code][json_key_turn_offer_status], callback_data=f'openOfferEdit_{id_offer}_{status_offer}_{page}')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['offer_edit_price_rate'], callback_data=f'offerEditPrice_{id_offer}_{page}')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['offer_edit_volume'], callback_data=f'offerEditVolume_{id_offer}_{page}')
    in4 = InlineKeyboardButton(text=_messages['button'][lang_code]['offer_edit_limits'], callback_data=f'offerEditLimits_{id_offer}_{page}')
    in5 = InlineKeyboardButton(text=_messages['button'][lang_code]['offer_edit_payment_methods'], callback_data=f'offerEditPaymentMethods_{id_offer}_{page}')
    in6 = InlineKeyboardButton(text=_messages['button'][lang_code]['offer_edit_payment_time'], callback_data=f'offerEditPaymentTime_{id_offer}_{page}')
    in7 = InlineKeyboardButton(text=_messages['button'][lang_code]['offer_delete'], callback_data=f'offerDelete_{id_offer}_{page}')
    in8 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f'myOffersPage_{page}')
    inline_markup.add(in1)
    inline_markup.add(in2)
    if status_offer == False:
        inline_markup.insert(in3)
    inline_markup.insert(in4)
    inline_markup.insert(in5)
    inline_markup.insert(in6)
    inline_markup.add(in7)
    inline_markup.add(in8)
    return inline_markup
        

async def edit_offer_crypto_rate(lang_code, select_fixed, id_offer, page):
    title_fixed_select = _messages['button'][lang_code]['currency_ad_rate']
    if select_fixed:
        title_fixed_select = f"• {_messages['button'][lang_code]['currency_ad_rate']} •"

    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=title_fixed_select, callback_data=f"newCryptoRateFixed_{id_offer}_{page}")
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['save_edit'], callback_data=f"saveEditPrice_{id_offer}_{page}")
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f"BackFromEditOffer_{id_offer}_{page}")
    inline_markup.add(in1)
    inline_markup.add(in2)
    inline_markup.add(in3)
    return inline_markup


async def edit_offer_amount_user_max(lang_code, amount, crypto, id_offer, page, _type='sell'):
    inline_matkup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['message_max_amount_ad_user'].format(amount, crypto),callback_data=f"{_type}AmountAdvertisementMax_{id_offer}_{page}")
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f"BackFromEditOffer_{id_offer}_{page}")    
    if _type == 'sell':
        inline_matkup.add(in1)
    inline_matkup.add(in2)
    return inline_matkup


async def back_to_offer(lang_code, id_offer, page):
    inline_matkup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f"BackFromEditOffer_{id_offer}_{page}")
    inline_matkup.add(in1)
    return inline_matkup


async def edit_offer_limit(lang_code, min_limit, user_limit, max_limit, id_offer, page):
    inline_keyboard = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=f'{min_limit}-{user_limit:.2f}', callback_data=f'EditOfferLimit_{min_limit}_{user_limit}')
    in2 = InlineKeyboardButton(text=f'{min_limit}-{max_limit}', callback_data=f'EditOfferLimit_{min_limit}_{max_limit}')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f"BackFromEditOffer_{id_offer}_{page}")
    inline_keyboard.add(in1)
    inline_keyboard.add(in2)
    inline_keyboard.add(in3)
    return inline_keyboard


async def edit_offer_payment(lang_code, id_user, currency, payment_id, datapro, id_offer, page):
    inline_markup = InlineKeyboardMarkup()

    numeb = await datapro.processing_select_payments_method(id_user, _all=False)
    
    for i in numeb:
        if i[0].payment_currency == currency:
            account_number = '*' + i[0].payment_data[-4:]
            if not i[0].payment_title is None:
                account_number = '- ' + i[0].payment_title

            in1 = InlineKeyboardButton(text=f'{i[0].payment_method} {account_number}', callback_data=f'editOfferPayment_{i[0].id}')
            for pay_id in payment_id:
                if in1.callback_data == f'editOfferPayment_{pay_id}':
                    in1.text = f'• {in1.text} •'
                else:
                    in1.text = f'{in1.text}'

            inline_markup.add(in1)
    
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['save_edit'], callback_data=f'saveEditOfferPayment_{id_offer}_{page}')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f"BackFromEditOffer_{id_offer}_{page}")
    inline_markup.add(in2)
    inline_markup.add(in3)
    return inline_markup


async def edit_offer_time(lang_code, _timer, id_offer, page):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['time_min'].format('15'), callback_data=f'newTimerDeals_15')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['time_min'].format('30'), callback_data=f'newTimerDeals_30')
    in3 = InlineKeyboardButton(text=_messages['button'][lang_code]['time_hour'].format('1'), callback_data=f'newTimerDeals_1')
    in4 = InlineKeyboardButton(text=_messages['button'][lang_code]['save_edit'], callback_data=f'saveEditOfferTime_{id_offer}_{page}')
    in5 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f"BackFromEditOffer_{id_offer}_{page}")

    if _timer == in1.callback_data:
        in1.text = f'• {in1.text} •'

    if _timer == in2.callback_data:
        in2.text = f'• {in2.text} •' 

    if _timer == in3.callback_data:
        in3.text = f'• {in3.text} •' 

    inline_markup.add(in1, in2, in3)
    inline_markup.add(in4)
    inline_markup.add(in5)
    return inline_markup


async def delete_offer(lang_code, id_offer, page):
    inline_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text=_messages['button'][lang_code]['yes'], callback_data=f'offerDeleteYes_{id_offer}_{page}')
    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['no'], callback_data=f"offerDeleteNo_{id_offer}_{page}")
    inline_markup.add(in1)
    inline_markup.add(in2)
    return inline_markup


async def select_sell_payment_method_type(lang_code, type_p2p_char, datapro, call_prev_data):
    inline_markup = InlineKeyboardMarkup()
    pay = await datapro.processing_select_payments()
    
    _index = 0
    if lang_code == 'ru':
        _index = 1

    for i in pay:
        if type_p2p_char in i[0].currency:
            in1 = InlineKeyboardButton(text=i[0].name.split('_')[_index], callback_data=f'p2pTypePayments_{call_prev_data}_{i[0].id}_sell')
            inline_markup.add(in1)

    in2 = InlineKeyboardButton(text=_messages['button'][lang_code]['back'], callback_data=f'sell')
    inline_markup.add(in2)

    return inline_markup
