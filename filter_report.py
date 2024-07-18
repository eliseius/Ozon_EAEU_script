from constants import FOREIGN_COUNTRIES_SHIPMENT


def filter_report(report):
    report_with_foreign_countries = filter_report_by_foreign_countries(report)
    report_with_universal_date = change_format_date(report_with_foreign_countries)
    dates_list = get_list_dates(report_with_universal_date)
    if dates_list:
        sorted_report_by_date = get_sorted_report_by_date(report_with_universal_date, dates_list)
        return sorted_report_by_date
    return None


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


def get_destination(region, city, item_sold):
    if city:
        return item_sold['city_delivery']
    elif region:
        return item_sold['region_delivery']
    return item_sold['cluster_delivery']


def change_format_date(report):
    for item in report:
        str_date_raw = item['shipment_date'].split(sep='T')
        item['shipment_date'] = str_date_raw[0]
    return report


def get_list_dates(report):
    dates = set()
    for item in report:
        dates.add(item['shipment_date'])

    return sorted(list(dates))


def get_sorted_report_by_date(report, dates_list):
    sorted_report = []
    for date in dates_list:
        for item in report:
            if date in item['shipment_date']:
                sorted_report.append(item)
    return sorted_report
