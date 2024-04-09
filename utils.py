import constants
import dateparser
import os

from telegram import ParseMode, ReplyKeyboardMarkup

from log import enter_for_log


def compose_keyboard():
    return ReplyKeyboardMarkup([['Сформировать отчёт',]])


def parse_date(input_date):
    parsed_date = dateparser.parse(input_date, settings = constants.DATEPARSER_SETTINGS)
    return parsed_date


def render_report(report_list):
    final_report = []
    for item in report_list:
        final_report.append(
            f'<b>Номер отправления:</b>  {item["posting_number"]}\n'
            f'<b>Дата отгрузки:</b>  {item["shipment_date"]}\n'
            f'<b>Цена в рублях:</b>  {item["price"]}р.\n'
            f'<b>Цена в долларах:</b>  {item["price_USD"]}$\n'
            f'<b>Наименование:</b>  {item["name"]}\n'
            f'<b>Количество:</b>  {item["quantity"]}\n'
            f'<b>Страна доставки:</b>  {item["country_delivery"]}\n'
            f'<b>Место назначения:</b>  {item["destination"]}\n'
            f'<b>Статус товара:</b>  {item["status"]}\n'
        )
    return '\n' .join(final_report)


def adapt_sum_post(report_list):
    sum_post = []
    for element in report_list:
        k, v = element[0], element[1]
        sum_post.append(
            f'{k} - {v} отправления(ий)'
        )
    return '\n'.join(sum_post)


def output_report(report, sum_post_in_city, update):
    limit_message = 10
    offset = 0
    while True:
        report_send = report[offset:limit_message]
        if len(report) > limit_message:
            update.message.reply_text(render_report(report_send), parse_mode = ParseMode.HTML)
            offset = limit_message
            limit_message += 10
        else:
            if report_send:
                update.message.reply_text(render_report(report_send), parse_mode = ParseMode.HTML)
            break

    update.message.reply_text(adapt_sum_post(sum_post_in_city))


def save_error_ozon(text):
    text = f'Возникла ошибка OZON\n{text}'
    error_log = f'Error OZON: {text}'
    write_error(text, error_log)


def save_error_currency(code):
    name_error = constants.LIST_ERROR_CURRENCY[code]
    text = f'Возникла ошибка ВАЛЮТЫ\n{code}: {name_error}'
    error_log = f'Error CURRENCY - {code}: {name_error}'
    write_error(text, error_log)


def write_error(name, error_log):
    enter_for_log(error_log, 'error')
    with open(constants.NAME_FILE_WITH_ERROR, 'w', encoding='utf-8') as file:
        file.write(name)


def output_error(update):
    with open(constants.NAME_FILE_WITH_ERROR, 'r', encoding='utf-8') as file:
        name_error = file.read()
    update.message.reply_text(name_error)
    os.remove(constants.LOCATE_FILE_WITH_ERROR)
