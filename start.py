from threading import Thread

from bot import main_bot
from update_db_currency import start_update_dbase


update_db = Thread(target=start_update_dbase, daemon=True)

update_db.start()
main_bot()