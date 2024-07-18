import os

from dotenv import load_dotenv


load_dotenv()

CURRENCY_API = os.getenv('CURRENCY_API')
DB_POSTGRESQL = os.getenv('DB_POSTGRESQL')
