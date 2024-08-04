import asyncio
import aiohttp

from src.processing import data_processing as datapro

async def update_cryptocurrency_price(parts: list) -> dict:
        crypto_currents = {}
        async with aiohttp.ClientSession() as session:
            for part in parts:
                try:
                    async with session.get(f"https://api.binance.com/api/v1/ticker/price?symbol={part}") as response:
                        data = await response.json()
                        price = data['price']
                        name = data['symbol']
                        crypto_currents[name] = float(price)
                except:
                    pass
            await session.close()
            return crypto_currents
    

async def while_method_update(flag):
    while flag:
        _listing_crypto = await datapro.processing_select_listing_crypto()
        _listpart_symbols = ('RUB', 'USDT', 'UAH', 'EUR')
        new_parts = []
        if _listing_crypto:
            for crypto in _listing_crypto:
                for part in _listpart_symbols:
                    new_parts.append(crypto + part)
        rates = await update_cryptocurrency_price(new_parts)
        print(rates)
        await datapro.processing_update_currency(rates)
        await asyncio.sleep(10)
