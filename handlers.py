from telegram import ParseMode

from utils import compose_keyboard


def start_bot(update, context):
    update.message.reply_text(
        'Для получения данных необходимо подключить <b>Seller API</b>,'
        ' ввести номер клиентского идентификатора (<b>Client ID</b>) и сгенерировать уникальный ключ (<b>API Key</b>).\n'
        'Как подключить <b>Seller API</b> и создать уникальный <b>API-ключ</b>, можно узнать по ссылке:\n'
        'https://seller-edu.ozon.ru/api-ozon/how-to-api\n'
        'Для продолжения нажмите "Ввести данные"',
        parse_mode = ParseMode.HTML,
        reply_markup = compose_keyboard('Ввести данные'),
    )


def has_incorrect_input(update, context):
    update.message.reply_text('Данная команда не поддерживается. Нажмите кнопку "Сформировать отчет"')
