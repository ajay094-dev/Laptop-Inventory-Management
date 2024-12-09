import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'laptop_inventory')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'rootuser')
    MYSQL_DB = os.getenv('MYSQL_DB', 'laptop_inventory')
    MYSQL_CURSORCLASS = 'DictCursor'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')