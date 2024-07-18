import requests

from datetime import datetime as dt
from datetime import timedelta as td

from db_currency.db import db_session
from db_currency.models import Currency

from db_currency.config_currency import CURRENCY_API
from db_currency.settings import CURRENCY, URL_CURRENCY


def fill_db(date):
    date_finish = dt.now().date()
    while True:
        date_send = date + td(days=1)
        if date_finish > date:
            add_data_in_db(date_send)
        else:
            break
        date = date_send


def transform_report(report):
    send_report = []
    short_report = {
        'date': report['date'],
        'currency': report['source'],
        'value': '%.2f' % float(report['quotes']['USDRUB']),
    }
    send_report.append(short_report)
    return send_report


def add_data_in_db(date):
    report_rates = get_exchange_rate(date)
    short_report = transform_report(report_rates)
    db_session.bulk_insert_mappings(Currency, short_report)
    db_session.commit()


def get_exchange_rate(str_date_send):
    for i in range(10):
        report = go_exchange_rates(str_date_send)
        if report and report['success']:
            return report
            break
    print('Ошибка получения данных валюты')
    print(report)
    return None


def go_exchange_rates(str_date_send):
    response = requests.get(f'{URL_CURRENCY}?access_key={CURRENCY_API}&date={str_date_send}&source={CURRENCY}')
    if response:
        exchange_rates = response.json()
        return exchange_rates
    else:
        print('Ошибка получения данных на сайте валюты')
        return None
