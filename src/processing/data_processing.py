import asyncio

from src.database.dbase import DExecute


async def processing_select_all_info_user(id_user: int) -> tuple:
    is_user_true = await DExecute.select_user_all_info(id_user)
    return is_user_true

async def processing_insert_new_user(*args: tuple) -> None:
    await DExecute.add_new_user(args=args)

async def processing_insert_new_ref(*args: tuple) -> None:
    await DExecute.add_new_ref(args=args)

async def processing_select_info_ban_user(id_user: int) -> tuple:
    info_ban = await DExecute.is_user_ban(id_user)
    return info_ban

async def processing_select_symbols():
    pass

async def processing_update_currency(currency: dict) -> None:
    await DExecute.update_currency(currency)

async def processing_select_all_currency() -> tuple:
    crypto_currency_rates = await DExecute.select_all_crypto_rates()
    return crypto_currency_rates

async def processing_select_one_crypto_rates(cryptocurrency_rate):
    crypto_rate = await DExecute.select_one_crypto_rates(cryptocurrency_rate)
    return crypto_rate

async def processing_select_listing_crypto() -> tuple:
    crypto_name = await DExecute.select_listing_crypto()
    return crypto_name

async def processing_select_crypto_balances(id_user: int) -> list:
    wallet_active = await DExecute.select_all_balances(id_user)
    return wallet_active 

async def prosessing_select_one_balance_user(id_user: int, crypto: str):
    balance_user = await DExecute.select_one_balance_user(id_user, crypto)
    return balance_user

async def processing_select_all_referrals(id_user: int) -> int:
    referrals = await DExecute.select_all_referrals(id_user)
    return referrals

async def processing_update_language_bot(id_user: int, lang_code: str) -> None:
    await DExecute.update_language_bot(id_user, lang_code)

async def processing_update_currency_bot(id_user: int, currency: str) -> None:
    await DExecute.update_currency_user_bot(id_user, currency)

async def processing_select_payments_method(id_user: int, _all=True) -> tuple:
    user_payment = await DExecute.select_payments_method(id_user, _all)
    return user_payment

async def processing_select_payments() -> tuple:
    payments = await DExecute.select_payments()
    return payments

async def processing_select_count_payments_user(id_user) -> (int | None):
    count_payments_user = await DExecute.select_count_payments_user(id_user)
    return count_payments_user

async def processing_add_payments_user(id_user: int,
                                payment_method: str,
                                payment_type: str,
                                payment_data: str,
                                payment_title: (None | str),
                                payment_currency: str) -> None:
    await DExecute.add_payments_user(id_user, payment_method, payment_type, payment_data, payment_title, payment_currency)


async def processing_select_user_p2p_market(id_user: int) -> tuple:
    user_market = await DExecute.select_user_p2p_market(id_user)
    return user_market

async def processing_add_user_p2p_market(id_user: int, agreement: bool, currency_p2p: str) -> None:
    await DExecute.add_user_p2p_market(id_user, agreement, currency_p2p)

async def processing_update_p2p_currency(id_user: int, currency_market: str) -> None:
    await DExecute.update_p2p_currency(id_user, currency_market)

async def processing_select_payment_info(id_user: int, _id: int) -> tuple:
    payment_info = await DExecute.select_payment_info(id_user, _id)
    return payment_info

async def processing_update_payment_title(id_user: int, _id: int, payment_title: str) -> None:
    await DExecute.update_payment_title(id_user, _id, payment_title)

async def processing_delete_payment(id_user: int, _id: int) -> None:
    await DExecute.delete_payment(id_user, _id)

async def processing_unban_user(id_user: int) -> None:
    await DExecute.delete_in_ban_user(id_user)

async def processing_add_advertisement(
            crypto: str,
            currency: str,
            crypto_rates: float,
            count,
            payment_method: list,
            amount_time: int,
            date: str,
            advertisement: bool,
            status: bool,
            id_user: int,
            type_add: str,
            limit_deals: list
            ) -> None:
    await DExecute.add_advertisement(
            crypto,
            currency,
            crypto_rates,
            count,
            payment_method,
            amount_time,
            date,
            advertisement,
            status,
            id_user,
            type_add,
            limit_deals)

async def processing_minus_crypto_balance(id_user: int, crypto: str, amount, method=True) -> None:
    await DExecute.update_crypto_balance(id_user, crypto, amount, method)

async def processing_select_advertisement_crypto(id_user: int, crypto: str) -> (tuple | None):
    amount = await DExecute.select_advertisement_crypto(id_user, crypto)
    return amount

async def processing_select_advertisement(id_user: int)  -> (tuple | None):
    advertisement = await DExecute.select_advertisement(id_user)
    return advertisement

async def processing_select_advertisement_user_method(crypto: str, currency: str, payment_method: str, type_add: str)  -> (tuple | None):
    advertisement_method = await DExecute.select_advertisement_user_method(crypto, currency, payment_method, type_add)
    return advertisement_method

async def processing_select_order_by_max_sell() -> (tuple | None):
    sell_max_rates = await DExecute.select_order_by_max_sell()
    return sell_max_rates

async def processing_select_offer(id_offer: int)  -> tuple:
    offer = await DExecute.select_offer(id_offer)
    return offer

async def processing_update_status_offer(id_user: int, id_offer: int, status_offer: bool) -> None:
    await DExecute.update_status_offer(id_user, id_offer, status_offer)

async def processing_update_crypto_rates_offer(id_user: int, id_offer: int, new_crypto_rate: int) -> None:
    await DExecute.update_crypto_rates_offer(id_user, id_offer, new_crypto_rate)

async def processing_update_crypto_volume_offer(id_user: int, id_offer: int, new_crypto_volume) -> None:
    await DExecute.update_crypto_volume(id_user, id_offer, new_crypto_volume)

async def processing_update_limit_offer(id_user: int, id_offer: int, new_min_limit: float, new_max_limit: float) -> None:
    await DExecute.update_crypto_limit(id_user, id_offer, new_min_limit, new_max_limit)

async def processing_update_payment_offer(id_user: int, id_offer: int, new_payment: str) -> None:
    await DExecute.update_crypto_payment(id_user, id_offer, new_payment)

async def processing_update_time_offer(id_user: int, id_offer: int, new_time: int) -> None:
    await DExecute.update_crypto_time(id_user, id_offer, new_time)

async def processing_delete_offer(id_user: int, id_offer: int) -> None:
    await DExecute.delete_offer(id_user, id_offer)

async def processing_select_limitations_crypto(name: str) -> (tuple | None):
    limits = await DExecute.select_limitations_crypto(name)
    return limits

async def processing_select_count_create_type_crypto_advertisement(cryptocurrency: str) -> (int | None):
    countCreateTypeCryptoAdvertisement = await DExecute.select_count_create_type_crypto_advertisement(cryptocurrency)
    return countCreateTypeCryptoAdvertisement