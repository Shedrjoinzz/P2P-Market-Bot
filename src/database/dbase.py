import asyncio

from datetime import datetime, timedelta

from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.exc import IntegrityError

from .dbsession import create_session_pool
from .model import Models
from src.system import check_crypto


class DExecute:
    async def is_user(id_user: int) -> bool:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Users).where(Models.Users.id_user == id_user))
                user = result.scalar_one_or_none()
                if user:
                    return True
                return False
            finally:
                await session.aclose()

                
    async def select_user_all_info(id_user: int) -> tuple:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Users).where(Models.Users.id_user == id_user))
                user = result.scalar_one_or_none()
                
                if user:
                    return user.id_user, user.name, user.lastname, user.username, user.positive_reviews, user.negative_reviews, user.date, user.currency, user.lang_code
            finally:
                await session.aclose()

    async def is_user_ban(id_user: int) -> tuple:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.BanSystem).where(Models.BanSystem.id_user == id_user))
                user = result.scalar_one_or_none()

                if user:
                    return user.id_user, user.discription, user.date
            finally:
                await session.aclose()

    async def add_new_user(args: tuple) -> bool:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(insert(Models.Users).values(id_user=args[0],
                                                            name=args[1],
                                                            lastname=args[2],
                                                            username=args[3],
                                                            positive_reviews=args[4],
                                                            negative_reviews=args[5],
                                                            date=args[6],
                                                            lang_code=args[7],
                                                            currency=args[8]))
                await session.commit()
                return True
            except IntegrityError:
                return False
            finally:
                await session.aclose()

    async def create_balance_new_user(args: tuple) -> bool:
        pass
    
    async def add_new_ref(args: tuple) -> bool:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(insert(Models.RefSystem).values(id_user=args[0],
                                                            id_ref=args[1],
                                                            date=args[2]))
                await session.commit()
                return True
            except IntegrityError:
                return False
            finally:
                await session.aclose()


    async def add_in_ban_user(id_user: int, discription: str, days: int) -> bool:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(insert(Models.BanSystem).values(id_user=id_user, discription=discription, date=datetime.now().date()+timedelta(days=days)))
                await session.commit()
                return True
            except IntegrityError:
                return False
            finally:
                await session.aclose()
            
    
    async def delete_in_ban_user(id_user: int) -> bool:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(delete(Models.BanSystem).where(Models.BanSystem.id_user == id_user))
                await session.commit()
            finally:
                await session.aclose()

    async def update_data_in_ban_user(id_user: int, discription: str, days: int) -> bool:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                select_date = await session.execute(select(Models.BanSystem).where(Models.BanSystem.id_user == id_user))
                user = select_date.scalar_one_or_none()
                if user:
                    if user.date <= user.date+timedelta(days=days):        
                        await session.execute(update(Models.BanSystem).where(Models.BanSystem.id_user == user.id_user).values(discription=discription, date=user.date+timedelta(days=days)))
                        return True
                    return False
                return None
            finally:
                await session.aclose()

    async def update_crypto_balance(id_user: int, crypto: int, amount, method: bool) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.CryptoBalance.balance).where(Models.CryptoBalance.id_user == id_user,
                                                                         Models.CryptoBalance.crypto == crypto))
                # print(result.scalar())
                balance = result.scalar_one()
                if method:
                    await session.execute(update(Models.CryptoBalance).where(Models.CryptoBalance.id_user == id_user,
                                                                            Models.CryptoBalance.crypto == crypto).values(balance=float(balance)-float(amount)))
                if method == False:
                    await session.execute(update(Models.CryptoBalance).where(Models.CryptoBalance.id_user == id_user,
                                                                            Models.CryptoBalance.crypto == crypto).values(balance=float(balance)+float(amount)))
                await session.commit()
            finally:
                await session.aclose()


    async def update_currency(set_list: dict) -> None:
        if set_list:
            pool = await create_session_pool()
            async with pool.begin() as session:
                try:
                    for name, price in set_list.items():
                        selected_data = await session.execute(select(Models.CryptocurreencyRates).where(Models.CryptocurreencyRates.crypto == name))
                        _data = selected_data.scalar_one_or_none()
                        if _data:
                            await session.execute(update(Models.CryptocurreencyRates).where(Models.CryptocurreencyRates.crypto == name).values(crypto=name, price=price))
                        else:
                            await session.merge(Models.CryptocurreencyRates(crypto=name, price=price))
                    await session.commit()
                finally:
                    await session.aclose()

    async def insert_new_order(args: tuple):
        pass

    async def select_listing_crypto() -> tuple:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Listing).where(Models.Listing.status == True))
                _cryptoname = result.all()
                _list = []
                if _cryptoname:
                    for i in _cryptoname:
                        _list.append(i[0].name)
                    return _list
            finally:
                await session.aclose()


    async def add_listing_crypto(name) -> bool:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Listing.name).where(Models.Listing.name == name)) # берём имя криптовалюты для проверки
                is_cryptoname = result.scalar()
                if is_cryptoname: # если есть криптовалюта в бд то НЕ добавляем
                    return False
                currenc = await check_crypto.check_current(name) # Если её нет в бд то проверяем на валидность отправляя запрос {name}RUB по API Binance
                if currenc: # если вернул курс криптовалюты в RUB то подтверждаем что он валидный и добавляем в бд
                    await session.execute(insert(Models.Listing).values(name=name, date=datetime.now().date(), status=True))
                    await session.commit()
                    return True # если всё прошло успешно
                return False # если не прошло проверку на валидность и т.п
            finally:
                await session.aclose() # закрываем ассинхронную сессию


    async def select_all_crypto_rates() -> tuple:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.CryptocurreencyRates.crypto, Models.CryptocurreencyRates.price))
                crypto_rates = result.fetchall()
                if crypto_rates:
                    return crypto_rates
                
            finally:
                await session.aclose()


    async def select_one_crypto_rates(cryptocurrency_rate):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.CryptocurreencyRates.price).where(Models.CryptocurreencyRates.crypto == cryptocurrency_rate))
                crypto_rate = result.scalar_one()
                if crypto_rate:
                    return crypto_rate

            finally:
                await session.aclose()


    async def select_all_balances(id_user: int) -> list:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.CryptoBalance).where(Models.CryptoBalance.id_user == id_user))
                balaces = result.all()
                _list = []
                if balaces:
                    for i in balaces:
                        _list.append((i[0].crypto, i[0].balance))
                    return _list
            finally:
                await session.aclose()


    async def select_one_balance_user(id_user: int, crypto: str):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.CryptoBalance).where(Models.CryptoBalance.id_user == id_user, Models.CryptoBalance.crypto == crypto))
                balance_user = result.scalar_one_or_none()
                if balance_user:
                    return balance_user.balance
                return None
            finally:
                await session.aclose()


    async def select_all_referrals(id_user: int) -> int:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(func.count(Models.RefSystem.id_user)).where(Models.RefSystem.id_ref == id_user))
                referrals = result.scalar_one_or_none()
                print(referrals)
                if referrals:
                    return referrals
                return 0
            finally:
                await session.aclose()

    async def update_language_bot(id_user: int, lang_code: str) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.Users).where(Models.Users.id_user == id_user).values(lang_code=lang_code))
                await session.commit()
            finally:
                await session.aclose()

    
    async def update_currency_user_bot(id_user: int, currency: str) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.Users).where(Models.Users.id_user == id_user).values(currency=currency))
                await session.commit()
            finally:
                await session.aclose()


    async def select_orders(type_add: str):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Orders).where(Models.Orders.type_order == type_add))
                orders = result.scalar_one_or_none()
                if orders:
                    return orders
            finally:
                await session.aclose()


    async def add_advertisement(
            crypto: str,
            currency: str,
            crypto_rates: float,
            count,
            payment_method: str,
            amount_time: int,
            date,
            advertisement: bool,
            status: bool,
            id_user: int,
            type_add: str,
            limit_deals: list,
            ) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(func.count()).where(Models.Advertisement.id_user == id_user))
                
                orders = result.scalar_one_or_none()

                await session.execute(insert(Models.Advertisement).values(
                    crypto=crypto,
                    currency=currency,
                    crypto_rates=crypto_rates,
                    count=count,
                    payment_method=payment_method,
                    amount_time=amount_time,
                    date=date,
                    advertisement=advertisement,
                    status=status,
                    id_user=id_user,
                    type_add=type_add,
                    limit_deals_min=limit_deals[0],
                    limit_deals_max=limit_deals[1]))
                await session.commit()
            finally:
                await session.aclose()


    async def select_payments_method(id_user: int, _all: bool) -> (tuple | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Payments).where(Models.Payments.id_user == id_user))
                if _all:
                    user_payment = result.scalar()
                    if user_payment:
                        return user_payment.payment_currency, user_payment.payment_data, user_payment.payment_method, user_payment.payment_title, user_payment.payment_type, user_payment.id

                if _all == False:
                    user_payment = result.fetchall()
                    return user_payment
            finally:
                await session.aclose()


    async def select_payment_info(id_user: int, _id: int) -> tuple:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Payments).where(Models.Payments.id_user == id_user, Models.Payments.id == _id))
                payment_info = result.scalar_one_or_none()
                if result:
                    return payment_info.payment_title, payment_info.payment_type, payment_info.payment_currency, payment_info.payment_method, payment_info.payment_data

            finally:
                await session.aclose()


    async def select_user_p2p_market(id_user: int) -> tuple:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.P2PMarketUser).where(Models.P2PMarketUser.id_user == id_user))
                p2p_user_market = result.scalar()

                if p2p_user_market:
                    return p2p_user_market.agreement, p2p_user_market.currency_market

            finally:
                await session.aclose()
    

    async def add_user_p2p_market(id_user: int, agreement: bool, currency_p2p: str) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(insert(Models.P2PMarketUser).values(id_user=id_user, agreement=agreement, currency_market=currency_p2p))
                await session.commit()
            finally:
                await session.aclose()


    async def update_p2p_currency(id_user: int, currency_p2p: str):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.P2PMarketUser).where(Models.P2PMarketUser.id_user == id_user).values(currency_market=currency_p2p))
                await session.commit()
            finally:
                await session.aclose()


    async def select_payments():
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.PaymentsAdmin))
                payments = result.fetchall()
                if payments:
                    return payments
            finally:
                await session.aclose()

    
    async def add_payments_user(id_user: int,
                                payment_method: str,
                                payment_type: str,
                                payment_data: str,
                                payment_title: (None | str),
                                payment_currency: str) -> None:
        
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(insert(Models.Payments).values(
                    id_user=id_user,
                    payment_method=payment_method,
                    payment_type=payment_type,
                    payment_data=payment_data,
                    payment_title=payment_title,
                    payment_currency=payment_currency))
                await session.commit()
            finally:
                await session.aclose()


    async def select_count_payments_user(id_user: int) -> (int | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(func.count()).where(Models.Payments.id_user == id_user))
                payments = result.scalar_one()
                if payments:
                    return payments
            finally:
                await session.aclose()

    
    async def update_payment_title(id_user: int, _id: int, payment_title: str) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.Payments).where(Models.Payments.id_user == id_user, Models.Payments.id == _id).values(payment_title=payment_title))
                await session.commit()
            finally:
                await session.aclose()


    async def delete_payment(id_user: int, _id: int) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(delete(Models.Payments).where(Models.Payments.id_user == id_user, Models.Payments.id == _id))
                await session.commit()
            finally:
                await session.aclose()


    async def select_advertisement_crypto(id_user: int, crypto: str) -> (tuple | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Advertisement).where(Models.Advertisement.id_user == id_user,
                                                                                  Models.Advertisement.crypto == crypto))
                amount = result.scalar()
                if amount:
                    return amount.count, amount.crypto
                
            finally:
                await session.aclose()

    async def select_advertisement(id_user: int) -> (tuple | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Advertisement).order_by(Models.Advertisement.id).where(Models.Advertisement.id_user == id_user))
                advertisement = result.fetchall()
                if advertisement:
                    return advertisement
            finally:
                await session.aclose()

    async def select_advertisement_user_method(crypto: str, currency: str, payment_method: str, type_add: str) -> (tuple | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                print("payment_method, type_add", payment_method, type_add)
                result = await session.execute(select(Models.Advertisement).order_by(Models.Advertisement.id).where(
                    Models.Advertisement.crypto == crypto,
                    Models.Advertisement.currency == currency,
                    Models.Advertisement.payment_method == payment_method,
                    Models.Advertisement.type_add == type_add
                    ))
                advertisement = result.fetchall()
                if advertisement:
                    return advertisement
            finally:
                await session.aclose()

    async def select_order_by_max_sell() -> (tuple | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Advertisement).order_by(Models.Advertisement.crypto_rates))
                sell_rates_max = result.fetchall()
                if sell_rates_max:
                    return sell_rates_max
            finally:
                await session.aclose()
    
    async def select_count_create_type_crypto_advertisement(cryptocurreny: str) -> (int | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Advertisement).where(Models.Advertisement.crypto == cryptocurreny))
                count_create_type_crypto = result.fetchall()
                if count_create_type_crypto:
                    return len(count_create_type_crypto)
            finally:
                await session.aclose()
    

    async def select_offer(id_offer: int) -> tuple:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.Advertisement).where(Models.Advertisement.id == id_offer))
                advertisement = result.scalar_one()
                if advertisement:
                    return (advertisement.id, advertisement.crypto, advertisement.currency, advertisement.crypto_rates,
                            advertisement.count, advertisement.payment_method, advertisement.amount_time, advertisement.date,
                            advertisement.advertisement, advertisement.status, advertisement.id_user, advertisement.type_add,
                            advertisement.limit_deals_min, advertisement.limit_deals_max)
            finally:
                await session.aclose()

    async def update_status_offer(id_user: int, id_offer: int, status_offer: bool) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                print(status_offer)
                await session.execute(update(Models.Advertisement).where(
                    Models.Advertisement.id_user == id_user,
                    Models.Advertisement.id == id_offer).values(advertisement=status_offer))
                await session.commit()
            finally:
                await session.aclose()

    async def update_crypto_rates_offer(id_user: int, id_offer: int, new_crypto_rate: int) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.Advertisement).where(
                    Models.Advertisement.id_user == id_user,
                    Models.Advertisement.id == id_offer).values(crypto_rates=new_crypto_rate))
                await session.commit()
            finally:
                await session.aclose()
    
    async def update_crypto_volume(id_user: int, id_offer: int, new_crypto_volume) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                print(new_crypto_volume)
                await session.execute(update(Models.Advertisement).where(
                    Models.Advertisement.id_user == id_user,
                    Models.Advertisement.id == id_offer).values(count=new_crypto_volume))
                await session.commit()
            finally:
                await session.aclose()
    
    async def update_crypto_limit(id_user: int, id_offer: int, new_min_limit: float, new_max_limit: float) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.Advertisement).where(
                    Models.Advertisement.id_user == id_user,
                    Models.Advertisement.id == id_offer).values(limit_deals_min=new_min_limit, limit_deals_max=new_max_limit))
                await session.commit()
            finally:
                await session.aclose()


    async def update_crypto_payment(id_user: int, id_offer: int, new_payment: str) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.Advertisement).where(
                    Models.Advertisement.id_user == id_user,
                    Models.Advertisement.id == id_offer).values(payment_method=new_payment))
                await session.commit()
            finally:
                await session.aclose()


    async def update_crypto_time(id_user: int, id_offer: int, new_time: int) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(update(Models.Advertisement).where(
                    Models.Advertisement.id_user == id_user,
                    Models.Advertisement.id == id_offer).values(amount_time=new_time))
                await session.commit()
            finally:
                await session.aclose()


    async def delete_offer(id_user: int, id_offer: int) -> None:
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                await session.execute(delete(Models.Advertisement).where(
                    Models.Advertisement.id_user == id_user,
                    Models.Advertisement.id == id_offer))
                await session.commit()
            finally:
                await session.aclose()

    
    async def select_limitations_crypto(name: str) -> (tuple | None):
        pool = await create_session_pool()
        async with pool.begin() as session:
            try:
                result = await session.execute(select(Models.LimitationsCrypto).where(Models.LimitationsCrypto.name == name))
                limits = result.scalar()
                if limits:
                    return limits.limit_buy, limits.limit_sell
            finally:
                await session.aclose()
