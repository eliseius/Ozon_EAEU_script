from datetime import datetime as dt

from db_currency.models import Currency
from log import enter_for_log
from utils import save_error_currency


def get_exchange_rate(date):
    try:
        query = Currency.query.filter(Currency.date==date).first()
        return query.value
    except:
        code = 800
        save_error_currency(code)
        return None


def get_report_with_currency(report):
    for item_sold in report:
        str_date = item_sold['shipment_date']
        date = dt.strptime(str_date, '%Y-%m-%d').date()
        rate = get_exchange_rate(date)
        if rate is not None:
            calcuation_usd = round(item_sold['price'] / float(rate), 2)
            item_sold['price'] = int(item_sold['price'])
            item_sold['price_USD'] = calcuation_usd
        else:
            date = item_sold['shipment_date']
            message = (f'Ошибка получения валюты. Дата -> {date}')
            enter_for_log(message, 'error')
            item_sold['price_USD'] = '-'
    return report
