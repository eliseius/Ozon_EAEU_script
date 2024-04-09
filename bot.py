import os

from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

from handlers import has_incorrect_input, start_bot
from log import enter_for_log
from anketa import (get_report_date_end, get_report_date_start, get_report_incorrect,
                    get_report_start)


def main_bot():
    ozon_bot = Updater(os.environ['OZON_BOT'], use_context = True)
    dp = ozon_bot.dispatcher
    report = ConversationHandler(
        entry_points = [MessageHandler(Filters.regex('^(Сформировать отчёт)$'), get_report_start)],
        states = {
            'period_start': [MessageHandler(Filters.text, get_report_date_start)],
            'period_end': [MessageHandler(Filters.text, get_report_date_end)],
        },
        fallbacks = [MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location, get_report_incorrect)],#Переписать этот обработчик
    )
    dp.add_handler(report)
    dp.add_handler(CommandHandler('start', start_bot))
    dp.add_handler(MessageHandler(Filters.text, has_incorrect_input))
    enter_for_log('BOT STARTER', 'info')
    ozon_bot.start_polling()
    ozon_bot.idle()


if __name__ == '__main__':
    main_bot()
