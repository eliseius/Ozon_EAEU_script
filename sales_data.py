from collections import Counter
from datetime import datetime as dt

from constants import OFFSET, STATUS_CATALOGUE
from filter_report import filter_report
from queries_in_db import get_report_with_currency
from raw_data_fbo import get_report_with_all_page_fbo
from raw_data_fbs import get_report_with_all_page_fbs


def get_sales_data(date_start, date_finish):#, status):
    str_datetime_start = dt.strftime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    str_datetime_finish = dt.strftime(date_finish, '%Y-%m-%dT%H:%M:%S.%fZ')

    report_fbs = get_report_with_all_page_fbs(str_datetime_start, str_datetime_finish, OFFSET)
    report_fbo = get_report_with_all_page_fbo(str_datetime_start, str_datetime_finish, OFFSET)
    report = report_fbs + report_fbo
    if report:
        sorted_report, sum_posts_in_country = get_report_on_shipments_to_countries(report)
        report_with_usd = get_report_with_currency(sorted_report)
        finall_report = decipher_the_status(report_with_usd)
        return finall_report, sum_posts_in_country
    return None, None


def get_report_on_shipments_to_countries(report):
    report_with_filter = filter_report(report)
    number_shipments_to_countries = get_number_shipments_to_countries(report_with_filter)
    sorted_report_by_country = get_sorted_report_by_country(report_with_filter, number_shipments_to_countries)

    return sorted_report_by_country, number_shipments_to_countries


def get_number_shipments_to_countries(report):
    clusters_delivery = []
    for position in report:
        clusters_delivery.append(position['country_delivery'])
    number_shipment_to_countries = Counter(clusters_delivery).most_common()
    return number_shipment_to_countries


def get_sorted_report_by_country(report, number_shipments_to_countries):
    sorted_report = []
    for element in number_shipments_to_countries:
        for item in report:
            if element[0] in item['country_delivery']:
                sorted_report.append(item)
    return sorted_report


def decipher_the_status(report):
    for item in report:
        status = item['status']
        if status in STATUS_CATALOGUE:
            item['stasus'] = STATUS_CATALOGUE[status]
    return report
