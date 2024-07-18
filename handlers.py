from utils import compose_keyboard


def start_bot(update, context):
    update.message.reply_text(
        'Для получения отчёта нажмите кнопку "Сформировать отчёт"',
        reply_markup = compose_keyboard(),
    )


def has_incorrect_input(update, context):
    update.message.reply_text('Данная команда не поддерживается. Нажмите кнопку "Сформировать отчет"')
