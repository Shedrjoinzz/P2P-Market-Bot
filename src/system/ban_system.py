# import aiogram
import asyncio
from src.database.dbase import DExecute

async def is_ban_user(id_user: int) -> bool:
    user = await DExecute.is_user_ban(id_user)
    if user:
        return True
    return False