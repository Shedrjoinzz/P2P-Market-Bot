from sqlalchemy import Column, BigInteger, Integer, Text, Date, Numeric, Boolean, DOUBLE_PRECISION
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Models:
    class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        id_user = Column(BigInteger)
        name = Column(Text)
        lastname = Column(Text)
        username = Column(Text)
        positive_reviews = Column(Integer)
        negative_reviews = Column(Integer)
        date = Column(Date)
        lang_code = Column(Text)
        currency = Column(Text)

    class RefSystem(Base):
        __tablename__ = 'ref_system'
        id = Column(Integer, primary_key=True)
        id_user = Column(BigInteger)
        id_ref = Column(BigInteger)
        date = Column(Date)

    class BanSystem(Base):
        __tablename__ = 'ban_system'
        id = Column(Integer, primary_key=True)
        id_user = Column(BigInteger)
        discription = Column(Text)
        date = Column(Date)

    class Deals(Base):
        __tablename__ = 'deals'
        id = Column(Integer, primary_key=True)
        id_one = Column(BigInteger)
        id_two = Column(BigInteger)

    class TransactionHistory(Base):
        __tablename__ = 'transaction_history'
        id = Column(Integer, primary_key=True)
        id_user = Column(BigInteger)
        name = Column(Text)
        name_partner = Column(Text)
        quantity = Column(BigInteger)
        _type = Column(Integer)

    class CryptocurreencyRates(Base):
        __tablename__ = 'cryptocurrency_rates'
        crypto = Column(Text)
        id = Column(Integer, primary_key=True, autoincrement=True)
        price = Column(DOUBLE_PRECISION)

    class Listing(Base):
        __tablename__ = 'crypto_listing'
        id = Column(Integer, primary_key=True)
        name = Column(Text)
        date = Column(Date)
        status = Column(Boolean)

    class CryptoBalance(Base):
        __tablename__ = 'crypto_balance'
        id = Column(Integer, primary_key=True)
        crypto = Column(Text)
        balance = Column(Numeric(precision=18, scale=8)) # точность 18, масштаб 8
        id_user = Column(BigInteger)

    class Orders(Base):
        __tablename__ = 'orders'
        id = Column(Integer, primary_key=True)
        id_user = Column(BigInteger)
        type_order = Column(Text)
        crypto = Column(Text)
        payment_method = Column(Text)
        crypto_rate = Column(DOUBLE_PRECISION)
        count = Column(Numeric(precision=18, scale=8))
        time_deals = Column(Integer)
        limit_deals = Column(Text)

    class Advertisement(Base):
        __tablename__ = 'advertisement'
        id = Column(Integer, primary_key=True)
        crypto = Column(Text)
        currency = Column(Text)
        crypto_rates = Column(DOUBLE_PRECISION)
        count = Column(Numeric(precision=18, scale=8))
        payment_method = Column(Text)
        amount_time = Column(Integer)
        date = Column(Date)
        advertisement = Column(Boolean)
        status = Column(Boolean)
        id_user = Column(BigInteger)
        type_add = Column(Text)
        limit_deals_min = Column(DOUBLE_PRECISION)
        limit_deals_max = Column(DOUBLE_PRECISION)

    class Payments(Base):
        __tablename__ = 'payments_sell_method'
        id = Column(Integer, primary_key=True)
        id_user = Column(BigInteger)
        payment_method = Column(Text)
        payment_type = Column(Text)
        payment_data = Column(Text)
        payment_title = Column(Text)
        payment_currency = Column(Text)

    class P2PMarketUser(Base):
        __tablename__ = 'p2p_market'
        id = Column(Integer, primary_key=True)
        id_user = Column(BigInteger)
        agreement = Column(Boolean)
        currency_market = Column(Text)

    class PaymentsAdmin(Base):
        __tablename__ = 'payments'
        id = Column(Integer, primary_key=True)
        name = Column(Text)
        type = Column(Text)
        currency = Column(Text)

    class LimitationsCrypto(Base):
        __tablename__ = 'limitations'
        id = Column(Integer, primary_key=True)
        name = Column(Text)
        limit_buy = Column(Numeric(precision=18, scale=8))
        limit_sell = Column(Numeric(precision=18, scale=8))
