from aiofile import async_open
from aiopath import AsyncPath
from datetime import datetime

async def log_exchange_command(command: str):
    log_file = AsyncPath("exchange.log")
    async with async_open(log_file, 'a') as afp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await afp.write(f"[{timestamp}] {command}\n")
