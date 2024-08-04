import asyncio
import aiohttp

async def check_current(crypto_name):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={crypto_name}RUB") as response:
                    data = await response.json()
                    price = data['price']
                    return price
        except:
            return False