import aiohttp
from datetime import datetime, timedelta
from .client import PrivatBankAPIClient
from .formatter import format_result

class ExchangeRateService:
    def __init__(self, currencies=None):
        self.api = PrivatBankAPIClient()
        self.currencies = currencies or ['USD', 'EUR']

    async def get_rates(self, days: int):
        days = min(days, 10)
        today = datetime.now()
        results = []

        async with aiohttp.ClientSession() as session:
            for i in range(days):
                date = today - timedelta(days=i)
                date_str = date.strftime("%d.%m.%Y")
                data = await self.api.fetch_exchange_rate(session, date_str)
                results.append(format_result(date_str, data, self.currencies))

        return results
