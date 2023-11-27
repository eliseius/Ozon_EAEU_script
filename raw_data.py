import json
import os
import requests

from datetime import datetime as dt

from constants import LIMIT, URL_OZON_FBS, URL_OZON_FBO
from filter_report import get_report_on_shipments_to_countries, make_short_report
from queries_in_db import get_report_with_currency
from utils import save_error_ozon


def get_sales_data(date_start, date_finish, status):
    offset = 0
    str_dt_start = dt.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_dt_finish = dt.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')

    report = get_report_with_all_page(str_dt_start, str_dt_finish, offset, status)
    sorted_report, sum_posts_in_country = get_report_on_shipments_to_countries(report)
    report_with_usd = get_report_with_currency(sorted_report)
    return report_with_usd, sum_posts_in_country


def get_report_with_all_page(str_datetime_start, str_datetime_finish, offset, status):
    report_pagination = []
    while True:
        sales_report = get_raw_sales_data_fbs(str_datetime_start, str_datetime_finish, LIMIT, offset, status)
        if sales_report is not None:
            short_report = make_short_report(sales_report)
            report_pagination.extend(short_report)
            if sales_report['result']['has_next']:
                offset += LIMIT
            else:
                break
        else:
            break
    return report_pagination


def get_raw_sales_data_fbs(datetime_start, datetime_finish, limit, offset, status):
    headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['OZON_API_KEY'],
               'Content-Type': 'application/json'}

    params = {
        'dir': 'asc',
        'filter': {
            'since': datetime_start,
            'status': status,
            'to': datetime_finish
        },
        'limit': limit,
        'offset': offset,
        'translit': True,
        'with': {
            'analytics_data': True,
            'financial_data': True,
        }
    }

    params = json.dumps(params)
    response = requests.post(URL_OZON_FBS, headers=headers, data=params)
    if response:
        try:
            sales_report = response.json()
            return sales_report
        except ValueError:
            print('Ошибка сформированных данных')
            code = 700
    else:
        print('Сетевая ошибка')
        code = response.status_code
    save_error_ozon(code)
    return None


# def get_raw_sales_data_fbo(datetime_start, datetime_finish, limit, offset, status):
#     headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['OZON_API_KEY'],
#                'Content-Type': 'application/json'}

#     params = {
#         'dir': 'asc',
#         'filter': {
#             'since': datetime_start,
#             'status': status,#Статусы для FBO другие
#             'to': datetime_finish
#         },
#         'limit': limit,
#         'offset': offset,
#         'translit': True,
#         'with': {
#             'analytics_data': True,
#             'financial_data': True,
#         }
#     }

#     params = json.dumps(params)
#     response = requests.post(URL_OZON_FBO, headers=headers, data=params)
#     if response:
#         try:
#             sales_report = response.json()
#             return sales_report
#         except ValueError:
#             print('Ошибка сформированных данных')
#             code = 700
#     else:
#         print('Сетевая ошибка')
#         code = response.status_code
#     save_error_ozon(code)
#     return None
