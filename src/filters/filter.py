import decimal
import asyncio


async def filter_decimal(num):
    try:
        dec = decimal.Decimal(num)
    except:
        pass
    
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = ''.join(str(d) for d in tup.digits)
    
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = '0.' + ('0'*zeros) + digits
    
    else:
        val = digits[:delta] + ('0'*tup.exponent) + '.' + digits[delta:]
    
    val = val.rstrip('0')
    
    if val[-1] == '.':
        val = val[:-1]
    
    return val


async def amount_balance_min_and_max(crypto, currency_user, crypto_rate):
    min_crypto_count_ad = None
    min_currency_count_ad = None

    if currency_user == "rub":
        min_crypto_count_ad = 100 / crypto_rate
        min_currency_count_ad = f"{(crypto_rate * min_crypto_count_ad):.2f}₽"
    
    if currency_user == "usd":
        min_crypto_count_ad = 1 / crypto_rate
        min_currency_count_ad = f"${float(crypto_rate * min_crypto_count_ad):.2f}"
        
    if crypto == "USDT":
        min_crypto_count_ad = 1

    return min_crypto_count_ad, min_currency_count_ad


async def limits(_currency, _crypto, crypto_rate, message_amount):
    min_limit = None
    max_limit = None
    _amount_currency = None
    message_amount_currency = None

    if _currency == 'RUB':
            min_limit = 100
            max_limit = 5_000_000
            message_amount_currency = f'{(crypto_rate * float(message_amount)):.2f}₽'
            _amount_currency = crypto_rate * float(message_amount)

    if _currency == 'USD':
        min_limit = 2
        max_limit = 100_000
        message_amount_currency = f'${(crypto_rate*float(message_amount)):.2f}'
        _amount_currency = crypto_rate * float(message_amount)
        if _crypto == 'USDT':
            message_amount_currency = f'${message_amount:.2f}'
            _amount_currency = message_amount

    return min_limit, max_limit, message_amount_currency, _amount_currency

async def one_crypto_rate(crypto, currency, datapro):
    crypto_rate = 0

    _crypto_rate = crypto+currency.replace("USD", "USDT")

    if currency.lower() == "usd" and crypto == "USDT":
        crypto_rate = 1



    if currency.lower() == "usd" and crypto != "USDT" or currency.lower() == "rub" or currency.lower() != "usd" and crypto == "USDT": 
        crypto_rate = await datapro.processing_select_one_crypto_rates(_crypto_rate)

    print(_crypto_rate, crypto_rate)
    return crypto_rate
