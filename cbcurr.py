import requests
from bs4 import BeautifulSoup

def fetch_currency_rates():
    url = 'https://cbr.ru/currency_base/daily/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        rates = {}
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            code = cols[1].text.strip()  # Букв. код (например, 'USD')
            units = float(cols[2].text.replace(',', '.'))
            rate = float(cols[4].text.replace(',', '.'))
            rates[code] = (units, rate)
        return rates
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки курсов валют: {e}")

def get_rate(from_code, to_code, rates):
    if from_code not in rates or to_code not in rates:
        raise ValueError("Неверный валютный код")
    units_from, rate_from = rates[from_code]
    units_to, rate_to = rates[to_code]
    rub_per_unit_from = rate_from / units_from
    rub_per_unit_to = rate_to / units_to
    return rub_per_unit_from, rub_per_unit_to


def convert_currency(amount, from_code, to_code, rates):
    rub_per_unit_from, rub_per_unit_to = get_rate(from_code, to_code, rates)
    amount_in_rub = amount * rub_per_unit_from
    result = amount_in_rub / rub_per_unit_to
    return result

def main():
    try:
        rates = fetch_currency_rates()
    except RuntimeError as e:
        print(e)
        return

    print("Доступные валюты:", ', '.join(rates.keys()))
    from_code = input("Введите исходную валюту (например, USD): ").upper()
    to_code = input("Введите целевую валюту (например, EUR): ").upper()
    try:
        amount = float(input("Введите сумму для конвертации: ").replace(',', '.'))
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        result = convert_currency(amount, from_code, to_code, rates)
        print(f"{amount} {from_code} = {result:.4f} {to_code}")
    except Exception as e:
        print(f"Ошибка конвертации: {e}")

if __name__ == "__main__":
    main()
