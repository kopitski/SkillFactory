import requests
import json

from config import currency

class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = currency[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')
        try:
            sym_key = currency[sym.lower()]
        except KeyError:
            raise APIException(f'Валюта {sym} не найдена!')
        if base_key == sym_key:
            raise APIException(f'Невозможно конвертировать одинаковые валюты: {base}!')
        try:
            int(amount)
        except ValueError:
            raise APIException(f'Неправильно ввели количество: {amount}')

        url = f'https://api.apilayer.com/fixer/convert?to={sym_key}&from={base_key}&amount={amount}'

        payload = {}
        headers = {
            "apikey": "6TESL4S9m67q6gZqaBFdf4CqRcAw8t8Z"
        }

        r = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(r.content)
        result = round(response['result'], 2)
        return result