from bs4 import BeautifulSoup as bs
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = bs(str(requests.get("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date).text), 'html.parser')
    valutes = response.find_all('valute')

    value_from = Decimal('1.0000')
    nominal_from = Decimal('1.0000')
    value_to = Decimal('1.0000')
    nominal_to = Decimal('1.0000')
    for valute in valutes:
        if valute.find('charcode').get_text() == cur_to:
            value_to = Decimal(valute.find('value').get_text().replace(',', '.'))
            nominal_to = Decimal(valute.find('nominal').get_text())
        if cur_from != 'RUR' and valute.find('charcode').get_text() == cur_from:
            value_from = Decimal(valute.find('value').get_text().replace(',', '.'))
            nominal_from = Decimal(valute.find('nominal').get_text())

    result = ((value_from / nominal_from) * amount * nominal_to) / value_to
    return result.quantize(Decimal('.0001'), rounding='ROUND_UP')
