from datetime import datetime as dt
from datetime import timedelta as td

from db_currency.utils_db import fill_db

from db_currency.settings import STR_DATE


def load_db():
    date = dt.strptime(STR_DATE, '%Y-%m-%d').date()
    date_start = date - td(days=1)
    fill_db(date_start)


if __name__ == '__main__':
    load_db()
