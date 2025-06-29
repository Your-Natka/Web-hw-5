import aiohttp
from datetime import datetime
from .exceptions import APIClientError

class PrivatBankAPIClient:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_exchange_rate(self, session: aiohttp.ClientSession, date: str):
        url = f"{self.BASE_URL}{date}"
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    raise APIClientError(f"Status {response.status}")
                return await response.json()
        except aiohttp.ClientError as e:
            raise APIClientError(str(e))
