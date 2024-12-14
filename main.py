import requests
from prettytable import PrettyTable

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # API для получения актуальных курсов валют


def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Проверка на успешность запроса
        data = response.json()
        return data['rates']
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None


def display_rates(rates):
    table = PrettyTable()
    table.field_names = ["Валюта", "Курс к USD", "Курс к RUB"]
    rub_to_usd = 1 / rates['RUB']  # Получаем курс RUB к USD
    for currency, rate in rates.items():
        if currency != 'USD':
            rub_rate = rate * rub_to_usd
            table.add_row([currency, f"{rate:.2f}", f"{rub_rate:.2f}"])
    print(table)


def convert_rub_to_usd(rates, amount_rub):
    usd_exchange_rate = rates['USD'] / rates['RUB']
    return amount_rub * usd_exchange_rate


def main():
    rates = get_exchange_rates()
    if rates is None:
        return

    display_rates(rates)

    while True:
        try:
            amount_rub = float(input("Введите сумму в RUB для конвертации в USD (или 'exit' для выхода): "))
            amount_usd = convert_rub_to_usd(rates, amount_rub)
            print(f"{amount_rub} RUB = {amount_usd:.2f} USD")
        except ValueError:
            print("Для выхода введите 'exit'.")
            break


if __name__ == "__main__":
    main()