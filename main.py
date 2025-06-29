import asyncio
import aiohttp
import sys
from datetime import datetime, timedelta


class PrivatBankAPIClient:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

    async def fetch_rates(self, session: aiohttp.ClientSession, date: str) -> dict:
        url = f"{self.BASE_URL}{date}"
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Network error for {date}: {e}")
            return {}


class ExchangeRateService:
    def __init__(self, client: PrivatBankAPIClient):
        self.client = client

    async def get_rates(self, days: int, currencies: list[str]) -> list[dict]:
        today = datetime.now()
        results = []
        async with aiohttp.ClientSession() as session:
            for i in range(days):
                date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
                data = await self.client.fetch_rates(session, date)
                if data.get('exchangeRate'):
                    rates = {}
                    for rate in data['exchangeRate']:
                        if rate.get('currency') in currencies:
                            rates[rate['currency']] = {
                                'sale': rate.get('saleRateNB'),
                                'purchase': rate.get('purchaseRateNB')
                            }
                    results.append({date: rates})
        return results


async def main():
    try:
        days = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Usage: python main.py <days> [additional currencies...]")
        return

    if not 1 <= days <= 10:
        print("Days must be between 1 and 10")
        return

    currencies = ['EUR', 'USD']
    if len(sys.argv) > 2:
        currencies.extend(sys.argv[2:])

    service = ExchangeRateService(PrivatBankAPIClient())
    rates = await service.get_rates(days, currencies)
    print(rates)


if __name__ == '__main__':
    asyncio.run(main())