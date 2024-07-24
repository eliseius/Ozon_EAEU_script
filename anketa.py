import constants
import os

from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from sales_data import get_sales_data
from utils import compose_keyboard, output_error, output_report, parse_date


def get_report_start(update, context):
    update.message.reply_text(
        'Введите ваш <b>Client ID</b>\n'
        'Идентификатор должен состоять только из цифр.\n'
        'Пример идентификатора: 228976',
        parse_mode = ParseMode.HTML,
        reply_markup = ReplyKeyboardRemove(),
    )
    return 'client_id'


def get_client_id(update, context):
    client_id = update.message.text
    if len(client_id) > 6:
        context.user_data['report'] = {'client_id': client_id}
    else:
        update.message.reply_text(
            'Введите корректный <b>Client ID</b>.'
            'Идентификатор должен состоять только из цифр. Пример идентификатора: 228976',
            parse_mode = ParseMode.HTML,
            )
        return 'client_id'
    
    update.message.reply_text(
        'Введите ваш <b>Api Key</b>\n'
        'Пример ключа: a608504t-61f0-4b81-bgh0-8022cladd876',
        parse_mode = ParseMode.HTML,
    )
    return 'api_key'


def get_api_key(update, context):
    api_key = update.message.text
    context.user_data['report']['api_key'] = api_key
    update.message.reply_text(
        'Введите дату начала периода в формате\n'
        '"год.месяц.день"',
    )
    return 'period_start'


def get_report_date_start(update, context):
    date_start = parse_date(update.message.text) # Дата должна соответствовать формату, это нужно проверять жестко
    if date_start is None:
        update.message.reply_text('Введите корректную дату начала периода')
        return 'period_start'
    context.user_data['report']['period_start'] = date_start

    update.message.reply_text(
        'Введите дату конца периода в формате\n'
        '"год.месяц.день"'
    )
    return 'period_end'


def get_report_date_end(update, context):
    date_end = parse_date(update.message.text)
    if date_end is None:
        update.message.reply_text('Введите корректную дату конца периода')
        return 'period_end'
    if date_end <= context.user_data['report']['period_start']:#Проверить ограничения по периоду за который можно запрашивать отчет
        update.message.reply_text('Дата конца периода не может быть раньше даты начала') #Нужно предложить заменить дату начала или начать все сначала
        return 'period_end'
    context.user_data['report']['period_end'] = date_end
    update.message.reply_text('Отчёт формируется...')



    print(context.user_data['report'])
    

    report_output, sum_post_in_city = get_sales_data(
        client_id=context.user_data['report']['client_id'],
        api_key=context.user_data['report']['api_key'],
        date_start=context.user_data['report']['period_start'],
        date_finish=context.user_data['report']['period_end'],
    )
    check_report(report_output, sum_post_in_city, update)

    update.message.reply_text(
        'Вы можете сформировать новый отчет',
        reply_markup = compose_keyboard('Ввести данные'),
    )
    return ConversationHandler.END


def get_report_incorrect(update, context):
    update.message.reply_text('Невозможно обработать объект!\nВведите корректные данные с клавиатуры')


def check_report(report, sum_post_in_city, update):
    if not report:
        if os.path.exists(constants.LOCATE_FILE_WITH_ERROR):
            output_error(update)
        else:
            update.message.reply_text('Нет заказов для отображения в отчёте. Попробуйте ввести другие данные')
    else:
        output_report(report, sum_post_in_city, update)
