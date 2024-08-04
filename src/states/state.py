from aiogram.dispatcher.filters.state import State, StatesGroup

class AdvertisementState(StatesGroup):
    id_user = State()
    type_add = State()
    crypto = State()
    currency = State()
    crypto_rates = State()
    count = State()
    limit_deals = State() # list deals limit
    payment_method = State()
    amount_time = State()
    date = State()
    advertisement = State()
    status = State()

class Payments(StatesGroup):
    currency = State()
    payment = State()
    _type = State()
    data = State()
    title = State()

class EditTitlePayment(StatesGroup):
    id_payment = State()

class EditOfferPrice(StatesGroup):
    id_offer = State()
    new_crypto_rate = State()
    page = State()

class EditOfferVolume(StatesGroup):
    id_offer = State()
    new_crypto_volume = State()
    page = State()

class EditOfferLimit(StatesGroup):
    id_offer = State()
    new_limit_deals = State()
    page = State()

class EditOfferPayment(StatesGroup):
    id_offer = State()
    new_payment = State()
    page = State()

class EditOfferTime(StatesGroup):
    id_offer = State()
    new_time = State()
    page = State()
    
