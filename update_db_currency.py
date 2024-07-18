import schedule
import time

from db_currency.models import Currency
from db_currency.utils_db import fill_db
from log import enter_for_log

from db_currency.config_currency import CURRENCY_API
from db_currency.settings import CURRENCY, URL_CURRENCY


def update_db():
    date_start = get_last_date()
    fill_db(date_start)


def get_last_date():
    try:
        query = Currency.query.order_by(Currency.date.desc()).first()
        return query.date
    except:
        message = (f'Ошибка подключения к БД')
        enter_for_log(message, 'error')
        return None
    

def start_update_dbase():
    minute_start = 1# изменить время после первого обращения в бд
    schedule.every(minute_start).minutes.do(update_db)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    start_update_dbase()