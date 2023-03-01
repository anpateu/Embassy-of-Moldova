import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    OWNER_ID = os.getenv('OWNER_ID')
    TOKEN = os.getenv('TOKEN')
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')