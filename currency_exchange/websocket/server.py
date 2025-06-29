from currency_exchange.currency.service import ExchangeRateService
from logger.logger import log_exchange_command

async def distribute(self, ws):
    async for message in ws:
        if message.startswith("exchange"):
            parts = message.strip().split()
            days = int(parts[1]) if len(parts) > 1 else 1
            service = ExchangeRateService()
            result = await service.get_rates(days)
            await log_exchange_command(message)
            await self.send_to_clients(f"{ws.name} запитав курс валют:\n{result}")
        else:
            await self.send_to_clients(f"{ws.name}: {message}")
