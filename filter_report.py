from collections import Counter

from constants import FOREIGN_COUNTRIES_SHIPMENT


def make_short_report(sales_report):
    all_item_sold = sales_report['result']['postings']
    short_report = []
    for one_item_sold in all_item_sold:
        inform_every_item_sold = {
            'posting_number': one_item_sold['posting_number'],
            'shipment_date': one_item_sold['shipment_date'],
            'price': float(one_item_sold['products'][0]['price']),
            'name': one_item_sold['products'][0]['name'],
            'quantity': one_item_sold['products'][0]['quantity'],
            'region_delivery': one_item_sold['analytics_data']['region'],
            'city_delivery': one_item_sold['analytics_data']['city'],
            'cluster_delivery': one_item_sold['financial_data']['cluster_to'],
        }
        short_report.append(inform_every_item_sold)
    return short_report


def get_report_on_shipments_to_countries(report):
    report_with_filter = filter_report_by_foreign_countries(report)
    # При слиянии отчетов FBO и FBS, тут нужно отсортировать по дате
    number_shipments_to_countries = get_number_shipments_to_countries(report_with_filter)
    sorted_report = get_sorted_report(report_with_filter, number_shipments_to_countries)

    return sorted_report, number_shipments_to_countries


def filter_report_by_foreign_countries(report):
    report_with_filter = []
    for item_sold in report:
        region = set(item_sold['region_delivery'].split())
        city = set(item_sold['city_delivery'].split())
        cluster = set(item_sold['cluster_delivery'].split())
        region.update(city, cluster)

        for country in FOREIGN_COUNTRIES_SHIPMENT:
            if region & FOREIGN_COUNTRIES_SHIPMENT[country]:
                item_sold['country_delivery'] = country
                item_sold['destination'] = get_destination(region, city, item_sold)
                report_with_filter.append(item_sold)
    return report_with_filter


def get_number_shipments_to_countries(report):
    clusters_delivery = []
    for position in report:
        clusters_delivery.append(position['country_delivery'])
    number_shipment_to_countries = Counter(clusters_delivery).most_common()
    return number_shipment_to_countries


def get_sorted_report(report, number_shipments_to_countries):
    sorted_report = []
    for element in number_shipments_to_countries:
        for item in report:
            if element[0] in item['country_delivery']:
                sorted_report.append(item)
    return sorted_report


def get_destination(region, city, item_sold):
    if city:
        return item_sold['city_delivery']
    elif region:
        return item_sold['region_delivery']
    return item_sold['cluster_delivery']

def get_Locality_buyer():
    pass