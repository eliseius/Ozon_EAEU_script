import os

from dotenv import load_dotenv


load_dotenv()

OZON_BOT_API = os.getenv('OZON_BOT_API')
OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
OZON_API = os.getenv('OZON_API')
