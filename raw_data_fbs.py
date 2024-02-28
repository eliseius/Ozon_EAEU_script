import json
import os
import requests

from constants import LIMIT, URL_OZON_FBS
from utils import save_error_ozon


def get_report_with_all_page_fbs(str_datetime_start, str_datetime_finish, offset):
    report_pagination = []
    while True:
        sales_report = get_raw_sales_data_fbs(str_datetime_start, str_datetime_finish, LIMIT, offset)
        if sales_report is not None:
            short_report = make_short_report_fbs(sales_report)
            report_pagination.extend(short_report)
            if sales_report['result']['has_next']:
                offset += LIMIT
            else:
                break
        else:
            break
    return report_pagination


def make_short_report_fbs(sales_report):
    all_item_sold = sales_report['result']['postings']
    short_report = []
    for one_item_sold in all_item_sold:
        for product in one_item_sold['products']:
            inform_every_item_sold = {
                'posting_number': one_item_sold['posting_number'],
                'shipment_date': one_item_sold['shipment_date'],
                'price': float(product['price']),
                'name': product['name'],
                'quantity': product['quantity'],
                'region_delivery': one_item_sold['analytics_data']['region'],
                'city_delivery': one_item_sold['analytics_data']['city'],
                'cluster_delivery': one_item_sold['financial_data']['cluster_to'],
                'status': one_item_sold['status'],
            }
            short_report.append(inform_every_item_sold)
    return short_report


def get_raw_sales_data_fbs(datetime_start, datetime_finish, limit, offset):
    headers = {'Client-Id': os.environ['OZON_CLIENT_ID'], 'Api-Key': os.environ['NEW_OZON_API_KEY'],
               'Content-Type': 'application/json'}

    params = {
        'dir': 'asc',
        'filter': {
            'since': datetime_start,
 #           'status': None,
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
    else:
        print('Сетевая ошибка')
    save_error_ozon(response.json()['message'])
    return None
