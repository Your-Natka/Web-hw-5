import sys
import asyncio
from currency.service import ExchangeRateService

async def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <кількість днів> [валюти через пробіл]")
        return

    try:
        days = int(sys.argv[1])
    except ValueError:
        print("Помилка: перший аргумент має бути числом")
        return

    currencies = sys.argv[2:] or ['USD', 'EUR']
    service = ExchangeRateService(currencies)
    try:
        result = await service.get_rates(days)
        
        # Форматований друк
        for day_data in result:
            for date, rates in day_data.items():
                print(f"Дата: {date}")
                for currency in currencies:
                    if currency in rates:
                        purchase = rates[currency].get('purchase', 'N/A')
                        sale = rates[currency].get('sale', 'N/A')
                        print(f"  Валюта: {currency}")
                        print(f"    Купівля: {purchase}")
                        print(f"    Продаж:  {sale}")
                print()  # порожній рядок між датами
        
    except Exception as e:
        print(f"Сталася помилка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
