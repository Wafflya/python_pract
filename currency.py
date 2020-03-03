from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + str(date)
    response = requests.get(url)  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')

    if cur_from != 'RUR':
        nom = int(soup.find('CharCode', text = cur_from).find_next_sibling('Nominal').string)
        value = Decimal(str(soup.find('CharCode', text = cur_from).find_next_sibling('Value').string.replace(',','.')))
        value_in_RUR = Decimal(nom*value*amount).quantize(amount)
    else:
        value_in_RUR = amount

    if cur_to == 'RUR':
        result = value_in_RUR
    else:
        nom = int(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string)
        value = Decimal(str(soup.find('CharCode', text=cur_to).find_next_sibling('Value').string.replace(',', '.')))
        result = Decimal(nom*value_in_RUR/value).quantize(amount)

    return result  # не забыть про округление до 4х знаков после запятой
